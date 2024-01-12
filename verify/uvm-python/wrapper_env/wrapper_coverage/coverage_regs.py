from uvm.macros.uvm_message_defines import uvm_info
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW
from cocotb_coverage.coverage import CoverPoint
from uvm.macros import uvm_component_utils
from wrapper_env.wrapper_item import wrapper_bus_item


class wrapper_cov_groups():
    def __init__(self, hierarchy, ip_regs_dict, irq_exist=False) -> None:
        self.hierarchy = hierarchy
        self.ip_regs_dict = ip_regs_dict
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        self.bus_cov(None, do_sampling=False)
        if irq_exist:
            self.irq_cov(None, do_sampling=False)

    def bus_cov(self, tr, do_sampling=True):
        cov_points = self._cov_points()

        @self.apply_decorators(decorators=cov_points)
        def sample(tr):
            pass
        if do_sampling:
            sample(tr)

    def irq_cov(self, tr, do_sampling=True):
        im_size = int(self.ip_regs_dict[3848]["size"])

        @CoverPoint(
            f"{self.hierarchy}.irq.irq",
            xf=lambda tr: tr.trg_irq,
            bins=[0, 1],
            bins_labels=["clear", "set"],
        )
        @CoverPoint(
            f"{self.hierarchy}.irq.irq_im",
            xf=lambda tr: (tr.trg_irq, self.ip_regs_dict[0xf08]["val"]),
            bins=[(i, 1 << j) for i in [0, 1] for j in range(im_size)],
            bins_labels=[f"({i}, flag{j})" for i in ["clear", "set"] for j in range(im_size)],
            rel=lambda val, b: val[1] == b[1] and val[0] == b[0]
        )
        def sample(tr):
            uvm_info("coverage", f"im_val: {self.ip_regs_dict[0xf08]['val']}", UVM_MEDIUM)
            pass
        if do_sampling:
            sample(tr)

    def _cov_points(self):
        cov_points = []
        for reg_addr, reg in self.ip_regs_dict.items():
            uvm_info("coverage", f"register: {reg['name']} reg_addr: {hex(reg_addr)}", UVM_MEDIUM)
            
            if "fields" not in reg:
                for access in ["write", "read"]:
                    # skip non write or read fields
                    if access == "write" and "w" not in reg["mode"]:
                        continue
                    if access == "read" and "r" not in reg["mode"]:
                        continue
                    reg_size = int(reg["size"])
                    if reg_size < 5:
                        cov_points.append(CoverPoint(
                            f"{self.hierarchy}.regs.{reg['name']}.{access}",
                            xf=lambda tr, reg_size=reg_size: (tr.addr & 0xffff, "write" if tr.kind == wrapper_bus_item.WRITE else "read", None if type(tr.data) is not int else (tr.data) & (1 << reg_size) - 1),
                            bins=[i for i in range(2**reg_size)],
                            bins_labels=[format(i, f'0{reg_size}b') for i in range(2 ** reg_size)],
                            rel=lambda val, b, address=reg_addr, access=access: val[2] is not None and val[1] == access and val[0] == address and val[2] == b
                            # rel=lambda val, b:  address
                        ))
                    else:
                        cov_points.append(CoverPoint(
                            f"{self.hierarchy}.regs.{reg['name']}.{access}",
                            xf=lambda tr, reg_size=reg_size: (tr.addr & 0xffff, "write" if tr.kind == wrapper_bus_item.WRITE else "read", None if type(tr.data) is not int else (tr.data ) & (1 << reg_size) - 1),
                            bins=[(1 << i, (1 << i + 1) - 1) if i != 0 else (0, 1) for i in range(reg_size)],
                            bins_labels=[f"from {hex(1 << i)} to {hex((1 << i + 1) - 1)}" if i != 0 else f"from {hex(0)} to {hex(1)}" for i in range(reg_size)],
                            rel=lambda val, b, address=reg_addr, access=access: val[2] is not None and val[1] == access and val[0] == address and b[0] <= val[2] <= b[1]
                        ))
            else:
                for field in reg["fields"]:
                    # skip non write or read fields
                    for access in ["write", "read"]:
                        if access == "write" and "w" not in reg["mode"]:
                            continue
                        if access == "read" and "r" not in reg["mode"]:
                            continue
                        field_size = int(field["bit_width"])
                        field_start = int(field["bit_offset"])
                        if field_size < 5:
                            cov_points.append(CoverPoint(
                                f"{self.hierarchy}.regs.{reg['name']}.{field['name']}.{access}",
                                xf=lambda tr, field_start=field_start, field_size=field_size: (tr.addr & 0xffff, "write" if tr.kind == wrapper_bus_item.WRITE else "read", None if type(tr.data) is not int else (tr.data >> field_start) & (1 << field_size) - 1),
                                bins=[i for i in range(2**field_size)],
                                bins_labels=[format(i, f'0{field_size}b') for i in range(2 ** field_size)],
                                rel=lambda val, b, address=reg_addr, access=access: val[2] is not None and val[1] == access and val[0] == address and val[2] == b
                                # rel=lambda val, b:  address
                            ))
                        else:
                            cov_points.append(CoverPoint(
                                f"{self.hierarchy}.regs.{reg['name']}.{field['name']}.{access}",
                                xf=lambda tr, field_start=field_start, field_size=field_size: (tr.addr & 0xffff, "write" if tr.kind == wrapper_bus_item.WRITE else "read", None if type(tr.data) is not int else (tr.data >> field_start) & (1 << field_size) - 1),
                                bins=[(1 << i, (1 << i + 1) - 1) if i != 0 else (0, 1) for i in range(field_size)],
                                bins_labels=[f"from {hex(1 << i)} to {hex((1 << i + 1) - 1)}" if i != 0 else f"from {hex(0)} to {hex(1)}" for i in range(field_size)],
                                rel=lambda val, b, address=reg_addr, access=access: val[2] is not None and val[1] == access and val[0] == address and b[0] <= val[2] <= b[1]
                            ))
        return cov_points

    def apply_decorators(self, decorators):
        def decorator_wrapper(func):
            for decorator in decorators:
                func = decorator(func)
            return func
        return decorator_wrapper


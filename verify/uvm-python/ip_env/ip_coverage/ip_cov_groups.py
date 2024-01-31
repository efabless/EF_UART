from uvm.macros.uvm_message_defines import uvm_info
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW
from cocotb_coverage.coverage import CoverPoint, CoverCross
from uvm.macros import uvm_component_utils
from ip_env.ip_item import ip_item


class ip_cov_groups():
    def __init__(self, hierarchy, regs) -> None:
        self.hierarchy = hierarchy
        self.regs = regs
        self.char_cov = self.all_word_char()
        self.ip_cov(None, do_sampling=False)

    def ip_cov(self, tr, do_sampling=True):
        @self.apply_decorators(decorators=self.char_cov)
        @CoverPoint(
            f"{self.hierarchy}.Prescaler",
            xf=lambda tr: (self.regs.read_reg_value("prescaler"), tr.direction),
            bins=[((0 if i == 0 else 1 << i * 4, (1 << (i * 4 + 4)) - 1), j) for i in range(4) for j in [ip_item.RX, ip_item.TX]],
            bins_labels=[((hex(0 if i == 0 else 1 << i * 4), hex((1 << (i * 4 + 4)) - 1)), "RX" if j == ip_item.RX else "TX") for i in range(4) for j in [ip_item.RX, ip_item.TX]],
            at_least=3,
            rel=lambda val, b: b[0][0] <= val[0] <= b[0][1] and val[1] == b[1]
        )
        @CoverPoint(
            f"{self.hierarchy}.Loopback",
            xf=lambda tr: (self.regs.read_reg_value("control") & 0b1000 == 0b1000),
            bins=[False, True],
            bins_labels=["loopback" if i else "normal" for i in [False, True]],
            at_least=3,
        )
        @CoverPoint(
            f"{self.hierarchy}.Glitch_fliter",
            xf=lambda tr: (self.regs.read_reg_value("control") & 0b10000 == 0b10000, tr.direction),
            bins=[(i,ip_item.RX) for i in [False, True]],
            bins_labels=["Flitered" if i else "not Flitered" for i in [False, True]],
            at_least=3,
        )
        @CoverPoint(
            f"{self.hierarchy}.Stopbits",
            xf=lambda tr: (self.regs.read_reg_value("config") & 0b10000 == 0b10000),
            bins=[False, True],
            bins_labels=["two stop bits" if i else "one stop bit" for i in [False, True]],
            at_least=3,
        )
        def sample(tr):
            uvm_info("coverage_ip", f"tr = {tr}", UVM_LOW)
        if do_sampling:
            sample(tr)

    def all_word_char(self):
        cov_points = []
        ranges = {9: [32, 16], 8: [16, 16], 7: [16, 8], 6: [8, 8], 5: [8, 4]}
        for direction in [ip_item.RX, ip_item.TX]:
            for word_len in range(5, 10):
                cov_points.append(CoverPoint(
                    f"{self.hierarchy}.{'TX' if direction == ip_item.TX else 'RX'}.Length{word_len}.Char",
                    xf=lambda tr: (tr.direction, tr.word_length, tr.char),
                    bins=[(i * ranges[word_len][0], i * ranges[word_len][0] + ranges[word_len][0]-1) for i in range(ranges[word_len][1])],
                    bins_labels=[f"from {hex(i * ranges[word_len][0])} to {hex(i * ranges[word_len][0] + ranges[word_len][0]-1)}" for i in range(ranges[word_len][1])],
                    rel=lambda val, b, direction=direction, word_len=word_len: direction == val[0] and word_len == val[1] and b[0] <= val[2] <= b[1]
                ))
                cov_points.append(CoverPoint(
                    f"{self.hierarchy}.{'TX' if direction == ip_item.TX else 'RX'}.Length{word_len}.Parity",
                    xf=lambda tr: (tr.direction, tr.word_length, tr.parity, (self.regs.read_reg_value("config") >> 5) & 0b111),
                    bins=[("None", 0), ("0", 1), ("1", 1), ("0", 2), ("1", 2), ("0", 4), ("1", 5)],
                    bins_labels=["None", "odd 0 parity", "odd 1 parity", "even 0 parity", "even 1 parity", "stick 0 parity", "stick 1 parity"],
                    rel=lambda val, b, direction=direction, word_len=word_len: direction == val[0] and word_len == val[1] and b[0] == val[2] and b[1] == val[3]
                ))
                cov_points.append(CoverCross(
                    f"{self.hierarchy}.{'TX' if direction == ip_item.TX else 'RX'}.Length{word_len}.Parity_char",
                    items=[
                        f"{self.hierarchy}.{'TX' if direction == ip_item.TX else 'RX'}.Length{word_len}.Parity",
                        f"{self.hierarchy}.{'TX' if direction == ip_item.TX else 'RX'}.Length{word_len}.Char",
                    ],
                ))
        return cov_points

    def apply_decorators(self, decorators):
        def decorator_wrapper(func):
            for decorator in decorators:
                func = decorator(func)
            return func
        return decorator_wrapper

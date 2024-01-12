from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.comps.uvm_monitor import UVMMonitor
from uvm.tlm1.uvm_analysis_port import UVMAnalysisPort
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb.triggers import Timer, RisingEdge
from wrapper_env.wrapper_item import wrapper_bus_item
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW


class wrapper_bus_monitor(UVMMonitor):
    def __init__(self, name="wrapper_bus_monitor", parent=None):
        super().__init__(name, parent)
        self.monitor_port = UVMAnalysisPort("monitor_port", self)
        self.tag = name

    def build_phase(self, phase):
        super().build_phase(phase)
        arr = []
        if (not UVMConfigDb.get(self, "", "wrapper_bus_if", arr)):
            uvm_fatal(self.tag, "No interface specified for self driver instance")
        else:
            self.sigs = arr[0]
        regs_arr = []
        if (not UVMConfigDb.get(self, "", "wrapper_regs", regs_arr)):
            uvm_fatal(self.tag, "No json file wrapper regs")
        else:
            self.regs = regs_arr[0]

    async def run_phase(self, phase):
        while True:
            tr = None
            # wait for a transaction
            while True:
                await self.sample_delay()
                if self.sigs.PSEL.value.binstr == "1" and self.sigs.PENABLE.value.binstr == "1":
                    break
            tr = wrapper_bus_item.type_id.create("tr", self)
            tr.kind = wrapper_bus_item.WRITE if self.sigs.PWRITE.value == 1 else wrapper_bus_item.READ
            tr.addr = self.sigs.PADDR.value.integer
            if tr.kind == wrapper_bus_item.WRITE:
                tr.data = self.sigs.PWDATA.value.integer
            else:
                try: 
                    tr.data = self.sigs.PRDATA.value.integer
                except ValueError:
                    tr.data = self.sigs.PRDATA.value.binstr
            self.monitor_port.write(tr)
            # update reg value #TODO: move this to the vip later
            self.regs.write_reg_value(tr.addr, tr.data)
            uvm_info(self.tag, "sampled APB transaction: " + tr.convert2string(), UVM_MEDIUM)

    async def sample_delay(self):
        await RisingEdge(self.sigs.PCLK)
        await Timer(1, "NS")

uvm_component_utils(wrapper_bus_monitor)

from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.comps.uvm_monitor import UVMMonitor
from uvm.tlm1.uvm_analysis_port import UVMAnalysisPort
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb.triggers import Edge, Timer
from wrapper_env.wrapper_item import wrapper_irq_item
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW


class wrapper_irq_monitor(UVMMonitor):
    def __init__(self, name="wrapper_irq_monitor", parent=None):
        super().__init__(name, parent)
        self.monitor_port = UVMAnalysisPort("wrapper_irq_monitor", self)
        self.tag = name

    def build_phase(self, phase):
        super().build_phase(phase)
        arr = []
        if (not UVMConfigDb.get(self, "", "wrapper_irq_if", arr)):
            uvm_fatal(self.tag, "No interface specified for self driver instance")
        else:
            self.sigs = arr[0]

    async def run_phase(self, phase):
        # if self.sigs.irq.value.binstr not in ["1", "0"]:  # ignore transition from x to 0
        #     await Edge(self.sigs.irq)
        #     await Timer(1, "NS")
        while True:
            tr = None
            await Edge(self.sigs.irq)
            tr = wrapper_irq_item.type_id.create("tr", self)
            if self.sigs.irq == 1:
                tr.trg_irq = 1
            else:
                tr.trg_irq = 0
            self.monitor_port.write(tr)
            uvm_info(self.tag, "sampled IRQ transaction: " + tr.convert2string(), UVM_MEDIUM)


uvm_component_utils(wrapper_irq_monitor)

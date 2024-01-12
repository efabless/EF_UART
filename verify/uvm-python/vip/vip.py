from uvm.base.uvm_component import UVMComponent
from uvm.macros import uvm_component_utils
from uvm.tlm1.uvm_analysis_port import UVMAnalysisImp
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW 
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_config_db import UVMConfigDb
from vip.model import EF_UART
from wrapper_env.wrapper_item import wrapper_bus_item
from uvm.tlm1.uvm_analysis_port import UVMAnalysisPort
from wrapper_env.wrapper_item import wrapper_bus_item


class vip(UVMComponent):
    def __init__(self, name="ip_coverage", parent=None):
        super().__init__(name, parent)
        self.analysis_imp = UVMAnalysisImp("vip_ap", self)
        self.wrapper_bus_export = UVMAnalysisPort("vip_bus_export", self)
        self.wrapper_irq_export = UVMAnalysisPort("vip_irq_export", self)
        self.ip_export = UVMAnalysisPort("vip_ip_export", self)
        self.model = None
        self.tag = "vip"

    def build_phase(self, phase):
        super().build_phase(phase)
        uvm_info(self.tag, "Vip built", UVM_MEDIUM)
        arr = []
        if (not UVMConfigDb.get(self, "", "wrapper_regs", arr)):
            uvm_fatal(self.tag, "No json file wrapper regs")
        else:
            self.regs = arr[0]
        self.model = EF_UART(self.regs)

    def connect_phase(self, phase):
        super().connect_phase(phase)
        uvm_info(self.tag, "Vip connected", UVM_MEDIUM)

    def write(self, tr):
        uvm_info(self.tag, "Vip write: " + tr.convert2string(), UVM_MEDIUM)
        if tr.kind == wrapper_bus_item.WRITE:
            self.model.write_register(tr.addr, tr.data)
            self.wrapper_bus_export.write(tr)
        elif tr.kind == wrapper_bus_item.READ:
            data = self.model.read_register(tr.addr)
            td = tr.do_clone()
            td.data = data
            self.wrapper_bus_export.write(td)


uvm_component_utils(vip)

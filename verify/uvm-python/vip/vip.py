from uvm.base.uvm_component import UVMComponent
from uvm.macros import uvm_component_utils
from uvm.tlm1.uvm_analysis_port import UVMAnalysisImp
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW 
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_config_db import UVMConfigDb
from vip.model import EF_UART
from wrapper_env.wrapper_item import wrapper_bus_item
from uvm.tlm1.uvm_analysis_port import UVMAnalysisExport
from uvm.macros.uvm_tlm_defines import uvm_analysis_imp_decl


uvm_analysis_imp_bus = uvm_analysis_imp_decl("_bus")
uvm_analysis_imp_ip = uvm_analysis_imp_decl("_ip")


class vip(UVMComponent):
    def __init__(self, name="ip_coverage", parent=None):
        super().__init__(name, parent)
        self.analysis_imp_bus = uvm_analysis_imp_bus("vip_ap_bus", self)
        self.analysis_imp_ip = uvm_analysis_imp_ip("vip_ap_ip", self)
        self.wrapper_bus_export = UVMAnalysisExport("vip_bus_export", self)
        self.wrapper_irq_export = UVMAnalysisExport("vip_irq_export", self)
        self.ip_export = UVMAnalysisExport("vip_ip_export", self)
        self.model = None
        self.tag = "vip"

    def build_phase(self, phase):
        super().build_phase(phase)
        self.model = EF_UART.type_id.create("model", self)

    def connect_phase(self, phase):
        super().connect_phase(phase)
        self.model.ip_export.connect(self.ip_export)

    def write_bus(self, tr):
        uvm_info(self.tag, "Vip write: " + tr.convert2string(), UVM_MEDIUM)
        if tr.kind == wrapper_bus_item.WRITE:
            self.model.write_register(tr.addr, tr.data)
            self.wrapper_bus_export.write(tr)
        elif tr.kind == wrapper_bus_item.READ:
            data = self.model.read_register(tr.addr)
            td = tr.do_clone()
            td.data = data
            self.wrapper_bus_export.write(td)

    def write_ip(self, tr):
        uvm_info(self.tag, "ip Vip write: " + tr.convert2string(), UVM_MEDIUM)
        self.model.tx_trig_event.set()
        pass


uvm_component_utils(vip)

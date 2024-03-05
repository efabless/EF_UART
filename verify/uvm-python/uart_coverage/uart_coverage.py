from uvm.base.uvm_component import UVMComponent
from uvm.macros import uvm_component_utils
from uvm.tlm1.uvm_analysis_port import UVMAnalysisImp
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW 
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.macros.uvm_tlm_defines import uvm_analysis_imp_decl
from uart_coverage.uart_cov_groups import ip_cov_groups
from EF_UVM.ip_env.ip_coverage.ip_coverage import ip_coverage


class uart_coverage(ip_coverage):
    """
    component that initialize the coverage groups and control when to sample the data.
    """
    def __init__(self, name="uart_coverage", parent=None):
        super().__init__(name, parent)

    def build_phase(self, phase):
        super().build_phase(phase)
        arr = []
        if (not UVMConfigDb.get(self, "", "bus_regs", arr)):
            uvm_fatal(self.tag, "No json file wrapper regs")
        else:
            regs = arr[0]
        self.cov_groups = ip_cov_groups("top.ip", regs)

    def write(self, tr):
        self.cov_groups.ip_cov(tr)


uvm_component_utils(uart_coverage)

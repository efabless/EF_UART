from uvm.base.uvm_component import UVMComponent
from uvm.macros import uvm_component_utils
from uvm.tlm1.uvm_analysis_port import UVMAnalysisImp
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW 
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.macros.uvm_tlm_defines import uvm_analysis_imp_decl
import os
import cocotb
from tabulate import tabulate
from wrapper_env.wrapper_item import wrapper_bus_item

uvm_analysis_imp_bus = uvm_analysis_imp_decl("_bus")
uvm_analysis_imp_irq = uvm_analysis_imp_decl("_irq")


class wrapper_logger(UVMComponent):
    def __init__(self, name="wrapper_logger", parent=None):
        super().__init__(name, parent)
        self.analysis_imp_bus = uvm_analysis_imp_bus("analysis_imp_bus", self)
        self.analysis_imp_irq = uvm_analysis_imp_irq("analysis_imp_irq", self)
        self.tag = name

    def build_phase(self, phase):
        super().build_phase(phase)
        arr = []
        if (not UVMConfigDb.get(self, "", "wrapper_regs", arr)):
            uvm_fatal(self.tag, "No json file wrapper regs")
        else:
            regs = arr[0]
        self.configure_logger()

    def write_bus(self, tr):
        uvm_info(self.tag, "get bus logging for " + tr.convert2string(), UVM_MEDIUM)
        self.bus_log(tr)
        pass

    def write_irq(self, tr):
        uvm_info(self.tag, "get irq logg for " + tr.convert2string(), UVM_MEDIUM)
        # self.cov_groups.irq_cov(tr)
        pass

    def configure_logger(self, logger_file="log.txt"):
        if not os.path.exists("loggers"):
            os.makedirs("loggers")
        self.logger_file = f"{os.getcwd()}/loggers/logger_bus.log"
        # # log the header
        self.bus_log(None, header_logged=True)

    def bus_log(self, transaction, header_logged=False):
        # Define a max width for each column
        col_widths = [20, 10, 10, 10]

        if header_logged:
            headers = [f"{'Time (ns)':<{col_widths[0]}}", f"{'Kind':<{col_widths[1]}}", f"{'Address':<{col_widths[2]}}", f"{'Data':<{col_widths[3]}}"]
            header = tabulate([], headers=headers, tablefmt="grid")
            with open(self.logger_file, 'w') as f:
                f.write(f"{header}\n")
        else:
            # Ensure each piece of data fits within the specified width
            sim_time = f"{cocotb.utils.get_sim_time(units='ns')} ns"
            operation = f"{'Write' if transaction.kind == wrapper_bus_item.WRITE else 'Read'}"
            address = f"{hex(transaction.addr)}"
            data = transaction.data if type(transaction.data) is not int else f"{hex(transaction.data)}"

            # Now, assemble your table_data with the pre-formatted fields
            table_data = [(f"{sim_time:<{col_widths[0]}}", f"{operation:<{col_widths[1]}}", f"{address:<{col_widths[2]}}", f"{data:<{col_widths[3]}}")]

            table = tabulate(table_data, tablefmt="grid")
            with open(self.logger_file, 'a') as f:
                f.write(f"{table}\n")


uvm_component_utils(wrapper_logger)

from uvm.base.uvm_component import UVMComponent
from uvm.macros import uvm_component_utils
from uvm.tlm1.uvm_analysis_port import UVMAnalysisImp
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW 
from uvm.base.uvm_config_db import UVMConfigDb
import os
import cocotb
from tabulate import tabulate
from ip_env.ip_item import ip_item


class ip_logger(UVMComponent):
    def __init__(self, name="ip_logger", parent=None):
        super().__init__(name, parent)
        self.analysis_imp = UVMAnalysisImp("logger_ap", self)
        self.tag = name

    def build_phase(self, phase):
        super().build_phase(phase)
        self.configure_logger()

    def write(self, tr):
        uvm_info(self.tag, "get bus logging for " + tr.convert2string(), UVM_MEDIUM)
        self.ip_log(tr)
        pass

    def configure_logger(self, logger_file="log.txt"):
        if not os.path.exists("loggers"):
            os.makedirs("loggers")
        self.logger_file = f"{os.getcwd()}/loggers/logger_ip.log"
        # # log the header
        self.ip_log(None, header_logged=True)

    def ip_log(self, transaction, header_logged=False):
        # Define a max width for each column
        col_widths = [20, 10, 10, 10]

        if header_logged:
            headers = [f"{'Time (ns)':<{col_widths[0]}}", f"{'Char':<{col_widths[1]}}"]
            header = tabulate([], headers=headers, tablefmt="grid")
            with open(self.logger_file, 'w') as f:
                f.write(f"{header}\n")
        else:
            # Ensure each piece of data fits within the specified width
            sim_time = f"{cocotb.utils.get_sim_time(units='ns')} ns"
            char = f"{transaction.char}"

            # Now, assemble your table_data with the pre-formatted fields
            table_data = [(f"{sim_time:<{col_widths[0]}}", f"{char:<{col_widths[1]}}")]

            table = tabulate(table_data, tablefmt="grid")
            with open(self.logger_file, 'a') as f:
                f.write(f"{table}\n")


uvm_component_utils(ip_logger)

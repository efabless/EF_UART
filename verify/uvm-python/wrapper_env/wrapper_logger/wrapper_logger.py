from uvm.base.uvm_component import UVMComponent
from uvm.macros import uvm_component_utils
from uvm.tlm1.uvm_analysis_port import UVMAnalysisImp
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW 
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
            self.regs = arr[0]
        self.configure_logger()

    def write_bus(self, tr):
        uvm_info(self.tag, "get bus logging for " + tr.convert2string(), UVM_HIGH)
        self.bus_log(tr)
        self.regs_log(tr)
        pass

    def write_irq(self, tr):
        uvm_info(self.tag, "get irq logg for " + tr.convert2string(), UVM_HIGH)
        # self.cov_groups.irq_cov(tr)
        pass

    def configure_logger(self, logger_file="log.txt"):
        if not os.path.exists("loggers"):
            os.makedirs("loggers")
        self.logger_file = f"{os.getcwd()}/loggers/logger_bus.log"
        self.logger_file_regs_w = f"{os.getcwd()}/loggers/regs_write.log"
        self.col_widths = [10, 10, 10, 10]
        # # log the header
        self.bus_log(None, header_logged=True)
        self.regs_log(None, header_logged=True)

    def bus_log(self, transaction, header_logged=False):
        # Define a max width for each column

        if header_logged:
            headers = [f"{'Time (ns)'}", f"{'Kind'}", f"{'Address'}", f"{'Data'}"]
            header = self.format_row(headers)
            with open(self.logger_file, 'w') as f:
                f.write(f"{header}\n")
        else:
            # Ensure each piece of data fits within the specified width
            sim_time = f"{cocotb.utils.get_sim_time(units='ns')} ns"
            operation = f"{'Write' if transaction.kind == wrapper_bus_item.WRITE else 'Read'}"
            address = f"{hex(transaction.addr)}"
            data = transaction.data if type(transaction.data) is not int else f"{hex(transaction.data)}"

            # Now, assemble your table_data with the pre-formatted fields
            table_data = [f"{sim_time}", f"{operation}", f"{address}", f"{data}"]

            table = self.format_row(table_data)
            with open(self.logger_file, 'a') as f:
                f.write(f"{table}\n")

    def regs_log(self, transaction, header_logged=False):
        # Define a max width for each column

        if header_logged:
            headers = [f"{'Time (ns)'}", f"{'Type'}", f"{'Name'}", f"{'Data'}"]
            header = self.format_row(headers)
            with open(self.logger_file_regs_w, 'w') as f:
                f.write(f"{header}\n")
        else:
            # Ensure each piece of data fits within the specified width
            sim_time = f"{cocotb.utils.get_sim_time(units='ns')} ns"
            # first write the register write then if it has fields
            the_type = "REG"
            Name = f"{self.regs.regs[transaction.addr]['name']}"
            data = f"{hex(transaction.data)}"
            # Now, assemble your table_data with the pre-formatted fields
            table_data = [f"{sim_time}", f"{the_type}", f"{Name}", f"{data}"]

            table = self.format_row(table_data)
            with open(self.logger_file_regs_w, 'a') as f:
                f.write(f"{table}\n")
            if "fields" in self.regs.regs[transaction.addr]:
                for field in self.regs.regs[transaction.addr]["fields"]:
                    the_type = "FIELD"
                    Name = f"{field['name']}"
                    data = f"{hex((transaction.data>>field['bit_offset'])&((1 << field['bit_width']) - 1))}"
                    # Now, assemble your table_data with the pre-formatted fields
                    table_data = [f"{sim_time}", f"{the_type}", f"{Name}", f"{data}"]
                    table = self.format_row(table_data)
                    with open(self.logger_file_regs_w, 'a') as f:
                        f.write(f"{table}\n")
                    

    def format_row(self, row_data):
        # Define a max width for each column
        for i in range(len(self.col_widths)):
            self.col_widths[i] = max(self.col_widths[i], len(row_data[i]) + 1)
        row_header = '+' + '+'.join('-' * (w) for w in self.col_widths) + '+'
        row = '|' + '|'.join(f"{item:{w}}" for item, w in zip(row_data, self.col_widths)) + '|'
        return row_header + "\n" + row



uvm_component_utils(wrapper_logger)

import cocotb

from uvm.comps import UVMTest
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info, uvm_warning
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.base.uvm_printer import UVMTablePrinter
from uvm.base.sv import sv
from uvm.base.uvm_object_globals import UVM_FULL, UVM_LOW
from uvm.base.uvm_globals import run_test
from top_env import top_env
from ip_files.ip_if import ip_if
from ip_files.wrapper_if import wrapper_bus_if, wrapper_irq_if
from cocotb.triggers import Timer
from wrapper_env.wrapper_seq_lib.write_read_regs import write_read_regs
from wrapper_env.wrapper_seq_lib.uart_tx_seq import uart_tx_seq
from cocotb_coverage.coverage import coverage_db
from caravel_cocotb.scripts.merge_coverage import merge_fun_cov
from wrapper_env.wrapper_regs import wrapper_regs
import os

@cocotb.test()
async def module_top(dut):
    pif = ip_if(dut)
    w_if = wrapper_bus_if(dut)
    w_irq_if = wrapper_irq_if(dut)
    example_base_test()
    UVMConfigDb.set(None, "*", "ip_if", pif)
    UVMConfigDb.set(None, "*", "wrapper_bus_if", w_if)
    UVMConfigDb.set(None, "*", "wrapper_irq_if", w_irq_if)
    # UVMConfigDb.set(None, "*", "json_file", "/home/rady/work/uvm_unit/EF_UART/EF_UART.json")
    head_path = f"{os.getcwd()}/../../"
    json_file = f"{head_path}/EF_UART.yaml"
    regs = wrapper_regs(json_file)
    UVMConfigDb.set(None, "*", "wrapper_regs", regs)
    UVMConfigDb.set(None, "*", "irq_exist", regs.get_irq_exist())
    await run_test()
    coverage_db.export_to_yaml(filename=f"{head_path}/verify/uvm-python/coverage.yalm")

    merge_fun_cov(f"{head_path}/verify/uvm-python/")
    # await Timer(999, "NS")


class example_base_test(UVMTest):
    def __init__(self, name="example_base_test", parent=None):
        super().__init__(name, parent)
        self.test_pass = True
        self.top_env = None
        self.printer = None

    def build_phase(self, phase):
        # UVMConfigDb.set(self, "example_tb0.wrapper_env.wrapper_agent.wrapper_sequencer.run_phase", "default_sequence", write_seq.type_id.get())
        super().build_phase(phase)
        # Enable transaction recording for everything
        UVMConfigDb.set(self, "*", "recording_detail", UVM_FULL)
        # Create the tb
        self.example_tb0 = top_env.type_id.create("example_tb0", self)
        # Create a specific depth printer for printing the created topology
        self.printer = UVMTablePrinter()
        self.printer.knobs.depth = -1

        arr = []
        if UVMConfigDb.get(None, "*", "ip_if", arr) is True:
            UVMConfigDb.set(self, "*", "ip_if", arr[0])
        else:
            # TODO: convert to uvm_fatal in the future
            uvm_fatal("NOVIF", "Could not get ip_if from config DB")

        if UVMConfigDb.get(None, "*", "wrapper_bus_if", arr) is True:
            UVMConfigDb.set(self, "*", "wrapper_bus_if", arr[0])
        else:
            # TODO: convert to uvm_fatal in the future
            uvm_fatal("NOVIF", "Could not get wrapper_bus_if from config DB")

    def end_of_elaboration_phase(self, phase):
        # Set verbosity for the bus monitor for this demo
        uvm_info(self.get_type_name(), sv.sformatf("Printing the test topology :\n%s", self.sprint(self.printer)), UVM_LOW)

    async def run_phase(self, phase):
        uvm_info("sequence", "Starting test", UVM_LOW)
        phase.raise_objection(self, "example_base_test OBJECTED")
        uvm_info("sequence", "after raise", UVM_LOW)
        wrapper_sqr = self.example_tb0.wrapper_env.wrapper_agent.wrapper_sequencer
        uvm_info("sequence", "after set seq", UVM_LOW)

        uvm_info("TEST_TOP", "Forking master_proc now", UVM_LOW)
        wrapper_seq = write_read_regs("write_read_regs")
        # wrapper_seq = uart_tx_seq("uart_tx_seq")
        await wrapper_seq.start(wrapper_sqr)
        await Timer(20, "US")
        phase.drop_objection(self, "example_base_test drop objection")

    # def extract_phase(self, phase):
    #     self.err_msg = ""
    #     if self.example_tb0.scoreboard0.sbd_error:
    #         self.test_pass = False
    #         self.err_msg += '\nScoreboard error flag set'
    #     if self.example_tb0.scoreboard0.num_writes == 0:
    #         self.test_pass = False
    #         self.err_msg += '\nnum_writes == 0 in scb'
    #     if self.example_tb0.scoreboard0.num_init_reads == 0:
    #         self.test_pass = False
    #         self.err_msg += '\nnum_init_reads == 0 in scb'


    def report_phase(self, phase):
        if self.test_pass:
            uvm_info(self.get_type_name(), "** UVM TEST PASSED **", UVM_LOW)
        else:
            uvm_fatal(self.get_type_name(), "** UVM TEST FAIL **\n" +
                self.err_msg)


uvm_component_utils(example_base_test)

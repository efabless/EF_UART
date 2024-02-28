import cocotb
from uvm.comps import UVMTest
from uvm import UVMCoreService
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.base.uvm_printer import UVMTablePrinter
from uvm.base.sv import sv
from uvm.base.uvm_object_globals import UVM_FULL, UVM_LOW, UVM_ERROR
from uvm.base.uvm_globals import run_test
from EF_UVM.top_env import top_env
from uart_interface.uart_if import uart_if
from EF_UVM.wrapper_env.wrapper_interface.wrapper_if import wrapper_apb_if, wrapper_irq_if, wrapper_ahb_if
from cocotb_coverage.coverage import coverage_db
from cocotb.triggers import Event, First
from EF_UVM.wrapper_env.wrapper_regs import wrapper_regs
from uvm.base.uvm_report_server import UVMReportServer
# seq
from EF_UVM.wrapper_env.wrapper_seq_lib.write_read_regs import write_read_regs
from uart_seq_lib.uart_tx_seq import uart_tx_seq
from uart_seq_lib.uart_config import uart_config
from uart_seq_lib.uart_rx_read import uart_rx_read
from uart_seq_lib.uart_rx_seq import uart_rx_seq
from uart_seq_lib.tx_length_parity_seq import tx_length_parity_seq
from uart_seq_lib.rx_length_parity_seq import rx_length_parity_seq, rx_length_parity_seq_wrapper
from uart_seq_lib.uart_prescalar_seq import uart_prescalar_seq_wrapper, uart_prescalar_seq
from uart_seq_lib.uart_loopback_seq import uart_loopback_seq
from uvm.base import UVMRoot

# override classes
from EF_UVM.ip_env.ip_agent.ip_driver import ip_driver
from uart_agent.uart_driver import uart_driver
from EF_UVM.ip_env.ip_agent.ip_monitor import ip_monitor
from uart_agent.uart_monitor import uart_monitor
from EF_UVM.vip.vip import VIP
from vip.vip import UART_VIP
from EF_UVM.scoreboard import scoreboard
from uart_scoreboard import uart_scoreboard
from EF_UVM.ip_env.ip_coverage.ip_coverage import ip_coverage
from uart_coverage.uart_coverage import uart_coverage
from EF_UVM.ip_env.ip_logger.ip_logger import ip_logger
from uart_logger.uart_logger import uart_logger

# 
from EF_UVM.wrapper_env.wrapper_agent.wrapper_ahb_driver import wrapper_ahb_driver
from EF_UVM.wrapper_env.wrapper_agent.wrapper_apb_driver import wrapper_apb_driver
from EF_UVM.wrapper_env.wrapper_agent.wrapper_ahb_monitor import wrapper_ahb_monitor
from EF_UVM.wrapper_env.wrapper_agent.wrapper_apb_monitor import wrapper_apb_monitor



@cocotb.test()
async def module_top(dut):
    # profiler = cProfile.Profile()
    # profiler.enable()
    arr = []
    # sv.value_plusargs('BUS_TYPE',arr)
    BUS_TYPE = cocotb.plusargs['BUS_TYPE']
    print(f"plusr agr value = {BUS_TYPE}")
    pif = uart_if(dut)
    if BUS_TYPE == "APB":
        w_if = wrapper_apb_if(dut)
    elif BUS_TYPE == "AHB":
        w_if = wrapper_ahb_if(dut)
    elif BUS_TYPE == "WISHBONE":
        w_if = wrapper_wishbone_if(dut)
    else:
        uvm_fatal("module_top", f"unknown bus type {BUS_TYPE}")
    w_irq_if = wrapper_irq_if(dut)
    UVMConfigDb.set(None, "*", "ip_if", pif)
    UVMConfigDb.set(None, "*", "wrapper_if", w_if)
    UVMConfigDb.set(None, "*", "wrapper_irq_if", w_irq_if)
    UVMConfigDb.set(None, "*", "json_file", "/home/rady/work/uvm_unit/EF_UART/EF_UART.json")
    yaml_file = []
    UVMRoot().clp.get_arg_values("+YAML_FILE=", yaml_file)
    yaml_file = yaml_file[0]
    regs = wrapper_regs(yaml_file)
    UVMConfigDb.set(None, "*", "wrapper_regs", regs)
    UVMConfigDb.set(None, "*", "irq_exist", regs.get_irq_exist())
    UVMConfigDb.set(None, "*", "insert_glitches", False)
    UVMConfigDb.set(None, "*", "collect_coverage", True)
    UVMConfigDb.set(None, "*", "disable_logger", False)
    test_path = []
    UVMRoot().clp.get_arg_values("+TEST_PATH=", test_path)
    test_path = test_path[0]
    await run_test()
    coverage_db.export_to_yaml(filename=f"{test_path}/coverage.yalm")
    # profiler.disable()
    # profiler.dump_stats("profile_result.prof")




class base_test(UVMTest):
    def __init__(self, name="base_test", parent=None):
        super().__init__(name, parent)
        self.test_pass = True
        self.top_env = None
        self.printer = None

    def build_phase(self, phase):
        # UVMConfigDb.set(self, "example_tb0.wrapper_env.wrapper_agent.wrapper_sequencer.run_phase", "default_sequence", write_seq.type_id.get())
        super().build_phase(phase)
        # override 
        self.set_type_override_by_type(ip_driver.get_type(), uart_driver.get_type())
        self.set_type_override_by_type(ip_monitor.get_type(), uart_monitor.get_type())
        self.set_type_override_by_type(VIP.get_type(), UART_VIP.get_type())
        self.set_type_override_by_type(scoreboard.get_type(), uart_scoreboard.get_type())
        self.set_type_override_by_type(ip_coverage.get_type(), uart_coverage.get_type())
        self.set_type_override_by_type(ip_logger.get_type(), uart_logger.get_type())
        BUS_TYPE = cocotb.plusargs['BUS_TYPE']
        if BUS_TYPE == "AHB":
            self.set_type_override_by_type(wrapper_apb_driver.get_type(), wrapper_ahb_driver.get_type())
            self.set_type_override_by_type(wrapper_apb_monitor.get_type(), wrapper_ahb_monitor.get_type())
        # self.set_type_override_by_type(ip_item.get_type(),uart_item.get_type())
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
            uvm_fatal("NOVIF", "Could not get ip_if from config DB")

        if UVMConfigDb.get(None, "*", "wrapper_if", arr) is True:
            UVMConfigDb.set(self, "*", "wrapper_if", arr[0])
        else:
            uvm_fatal("NOVIF", "Could not get wrapper_if from config DB")
        # set max number of uvm errors 
        server = UVMReportServer()
        server.set_max_quit_count(3)
        UVMCoreService.get().set_report_server(server)


    def end_of_elaboration_phase(self, phase):
        # Set verbosity for the bus monitor for this demo
        uvm_info(self.get_type_name(), sv.sformatf("Printing the test topology :\n%s", self.sprint(self.printer)), UVM_LOW)

    def start_of_simulation_phase(self, phase):
        self.wrapper_sqr = self.example_tb0.wrapper_env.wrapper_agent.wrapper_sequencer
        self.ip_sqr = self.example_tb0.ip_env.ip_agent.ip_sequencer

    async def run_phase(self, phase):
        uvm_info("sequence", "Starting test", UVM_LOW)

    def extract_phase(self, phase):
        super().check_phase(phase)
        server = UVMCoreService.get().get_report_server()
        errors = server.get_severity_count(UVM_ERROR)
        if errors > 0:
            uvm_fatal("FOUND ERRORS", "There were " + str(errors) + " UVM_ERRORs in the test")

    def report_phase(self, phase):
        uvm_info(self.get_type_name(), "report_phase", UVM_LOW)
        if self.test_pass:
            uvm_info(self.get_type_name(), "** UVM TEST PASSED **", UVM_LOW)
        else:
            uvm_fatal(self.get_type_name(), "** UVM TEST FAIL **\n" +
                self.err_msg)


uvm_component_utils(base_test)


class TX_StressTest(base_test):
    def __init__(self, name="TX_StressTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def run_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        wrapper_seq = uart_tx_seq("uart_tx_seq")
        wrapper_seq.monitor = self.example_tb0.ip_env.ip_agent.monitor
        await wrapper_seq.start(self.wrapper_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(TX_StressTest)


class RX_StressTest(base_test):
    def __init__(self, name="RX_StressTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def run_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        ip_seq_rx = uart_rx_seq("uart_rx_seq")
        wrapper_config_uart = uart_config()
        wrapper_rx_read = uart_rx_read()
        await wrapper_config_uart.start(self.wrapper_sqr)
        for _ in range(10):
            await ip_seq_rx.start(self.ip_sqr)
            await wrapper_rx_read.start(self.wrapper_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(RX_StressTest)


class LoopbackTest(base_test):
    def __init__(self, name="LoopbackTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def run_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        wrapper_seq = uart_loopback_seq("uart_loopback_seq")
        wrapper_seq.monitor = self.example_tb0.ip_env.ip_agent.monitor
        await wrapper_seq.start(self.wrapper_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(LoopbackTest)


class PrescalarStressTest(base_test):
    def __init__(self, name="PrescalarTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def run_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        handshake_event = Event("handshake_event")
        ip_seq = uart_prescalar_seq(handshake_event)
        wrapper_seq = uart_prescalar_seq_wrapper(handshake_event)
        wrapper_seq.tx_seq_obj.monitor = self.example_tb0.ip_env.ip_agent.monitor
        wrapper_seq_thread = await cocotb.start(wrapper_seq.start(self.wrapper_sqr))
        ip_seq_thread = await cocotb.start(ip_seq.start(self.ip_sqr))
        await First(ip_seq_thread, wrapper_seq_thread)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(PrescalarStressTest)


class LengthParityTXStressTest(base_test):
    def __init__(self, name="LengthParityTXStressTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def run_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        wrapper_seq = tx_length_parity_seq()
        wrapper_seq.tx_seq_obj.monitor = self.example_tb0.ip_env.ip_agent.monitor
        await wrapper_seq.start(self.wrapper_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(LengthParityTXStressTest)


class LengthParityRXStressTest(base_test):
    def __init__(self, name="LengthParityRXStressTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def run_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        handshake_event = Event("handshake_event")
        wrapper_seq = rx_length_parity_seq_wrapper(handshake_event)
        ip_seq = rx_length_parity_seq(handshake_event)
        wrapper_seq_thread = await cocotb.start(wrapper_seq.start(self.wrapper_sqr))
        ip_seq_thread = await cocotb.start(ip_seq.start(self.ip_sqr))
        await First(ip_seq_thread, wrapper_seq_thread)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(LengthParityRXStressTest)


class WriteReadRegsTest(base_test):
    def __init__(self, name="WriteReadRegsTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def run_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        wrapper_seq = write_read_regs()
        await wrapper_seq.start(self.wrapper_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(WriteReadRegsTest)

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
from EF_UVM.bus_env.bus_interface.bus_if import (
    bus_apb_if,
    bus_irq_if,
    bus_ahb_if,
    bus_wb_if,
)
from cocotb_coverage.coverage import coverage_db
from cocotb.triggers import Event, First
from EF_UVM.bus_env.bus_regs import bus_regs
from uvm.base.uvm_report_server import UVMReportServer

# seq
from EF_UVM.bus_env.bus_seq_lib.write_read_regs import write_read_regs
from uart_seq_lib.uart_tx_seq import uart_tx_seq
from uart_seq_lib.uart_config import uart_config
from uart_seq_lib.uart_rx_read import uart_rx_read
from uart_seq_lib.uart_rx_seq import uart_rx_seq
from uart_seq_lib.tx_length_parity_seq import tx_length_parity_seq
from uart_seq_lib.rx_length_parity_seq import (
    rx_length_parity_seq,
    rx_length_parity_seq_wrapper,
)
from uart_seq_lib.uart_prescalar_seq import (
    uart_prescalar_seq_wrapper,
    uart_prescalar_seq,
)
from uart_seq_lib.uart_loopback_seq import uart_loopback_seq
from uvm.base import UVMRoot

# override classes
from EF_UVM.ip_env.ip_agent.ip_driver import ip_driver
from uart_agent.uart_driver import uart_driver
from EF_UVM.ip_env.ip_agent.ip_monitor import ip_monitor
from uart_agent.uart_monitor import uart_monitor
from EF_UVM.ref_model.ref_model import ref_model
from ref_model.ref_model import UART_VIP
from EF_UVM.scoreboard import scoreboard
from uart_scoreboard import uart_scoreboard
from EF_UVM.ip_env.ip_coverage.ip_coverage import ip_coverage
from uart_coverage.uart_coverage import uart_coverage
from EF_UVM.ip_env.ip_logger.ip_logger import ip_logger
from uart_logger.uart_logger import uart_logger

#
from EF_UVM.bus_env.bus_agent.bus_ahb_driver import bus_ahb_driver
from EF_UVM.bus_env.bus_agent.bus_apb_driver import bus_apb_driver
from EF_UVM.bus_env.bus_agent.bus_wb_driver import bus_wb_driver
from EF_UVM.bus_env.bus_agent.bus_ahb_monitor import bus_ahb_monitor
from EF_UVM.bus_env.bus_agent.bus_apb_monitor import bus_apb_monitor
from EF_UVM.bus_env.bus_agent.bus_wb_monitor import bus_wb_monitor

from EF_UVM.base_test import base_test


@cocotb.test()
async def module_top(dut):
    # profiler = cProfile.Profile()
    # profiler.enable()
    BUS_TYPE = cocotb.plusargs["BUS_TYPE"]
    print(f"plusr agr value = {BUS_TYPE}")
    pif = uart_if(dut)
    if BUS_TYPE == "APB":
        w_if = bus_apb_if(dut)
    elif BUS_TYPE == "AHB":
        w_if = bus_ahb_if(dut)
    elif BUS_TYPE == "WISHBONE":
        w_if = bus_wb_if(dut)
    else:
        uvm_fatal("module_top", f"unknown bus type {BUS_TYPE}")
    w_irq_if = bus_irq_if(dut)
    UVMConfigDb.set(None, "*", "ip_if", pif)
    UVMConfigDb.set(None, "*", "bus_if", w_if)
    UVMConfigDb.set(None, "*", "bus_irq_if", w_irq_if)
    UVMConfigDb.set(
        None, "*", "json_file", "/home/rady/work/uvm_unit/EF_UART/EF_UART.json"
    )
    yaml_file = []
    UVMRoot().clp.get_arg_values("+YAML_FILE=", yaml_file)
    yaml_file = yaml_file[0]
    regs = bus_regs(yaml_file)
    UVMConfigDb.set(None, "*", "bus_regs", regs)
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


class uart_base_test(base_test):
    def __init__(self, name="uart_base_test", parent=None):
        BUS_TYPE = cocotb.plusargs["BUS_TYPE"]
        super().__init__(name, bus_type=BUS_TYPE, parent=parent)
        self.tag = name

    def build_phase(self, phase):
        super().build_phase(phase)
        # override
        self.set_type_override_by_type(ip_driver.get_type(), uart_driver.get_type())
        self.set_type_override_by_type(ip_monitor.get_type(), uart_monitor.get_type())
        self.set_type_override_by_type(ref_model.get_type(), UART_VIP.get_type())
        self.set_type_override_by_type(
            scoreboard.get_type(), uart_scoreboard.get_type()
        )
        self.set_type_override_by_type(ip_coverage.get_type(), uart_coverage.get_type())
        self.set_type_override_by_type(ip_logger.get_type(), uart_logger.get_type())


uvm_component_utils(uart_base_test)


class TX_StressTest(uart_base_test):
    def __init__(self, name="TX_StressTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def main_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        bus_seq = uart_tx_seq("uart_tx_seq")
        bus_seq.monitor = self.top_env.ip_env.ip_agent.monitor
        await bus_seq.start(self.bus_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(TX_StressTest)


class RX_StressTest(uart_base_test):
    def __init__(self, name="RX_StressTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def main_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        ip_seq_rx = uart_rx_seq("uart_rx_seq")
        bus_config_uart = uart_config()
        bus_rx_read = uart_rx_read()
        await bus_config_uart.start(self.bus_sqr)
        for _ in range(10):
            await ip_seq_rx.start(self.ip_sqr)
            await bus_rx_read.start(self.bus_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(RX_StressTest)


class LoopbackTest(uart_base_test):
    def __init__(self, name="LoopbackTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def main_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        bus_seq = uart_loopback_seq("uart_loopback_seq")
        bus_seq.monitor = self.top_env.ip_env.ip_agent.monitor
        await bus_seq.start(self.bus_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(LoopbackTest)


class PrescalarStressTest(uart_base_test):
    def __init__(self, name="PrescalarTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def main_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        handshake_event = Event("handshake_event")
        ip_seq = uart_prescalar_seq(handshake_event)
        bus_seq = uart_prescalar_seq_wrapper(handshake_event)
        bus_seq.tx_seq_obj.monitor = self.top_env.ip_env.ip_agent.monitor
        bus_seq_thread = await cocotb.start(bus_seq.start(self.bus_sqr))
        ip_seq_thread = await cocotb.start(ip_seq.start(self.ip_sqr))
        await First(ip_seq_thread, bus_seq_thread)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(PrescalarStressTest)


class LengthParityTXStressTest(uart_base_test):
    def __init__(self, name="LengthParityTXStressTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def main_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        bus_seq = tx_length_parity_seq()
        bus_seq.tx_seq_obj.monitor = self.top_env.ip_env.ip_agent.monitor
        await bus_seq.start(self.bus_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(LengthParityTXStressTest)


class LengthParityRXStressTest(uart_base_test):
    def __init__(self, name="LengthParityRXStressTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def main_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        handshake_event = Event("handshake_event")
        bus_seq = rx_length_parity_seq_wrapper(handshake_event)
        ip_seq = rx_length_parity_seq(handshake_event)
        bus_seq_thread = await cocotb.start(bus_seq.start(self.bus_sqr))
        ip_seq_thread = await cocotb.start(ip_seq.start(self.ip_sqr))
        await First(ip_seq_thread, bus_seq_thread)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(LengthParityRXStressTest)


class WriteReadRegsTest(uart_base_test):
    def __init__(self, name="WriteReadRegsTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def main_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        bus_seq = write_read_regs()
        await bus_seq.start(self.bus_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(WriteReadRegsTest)

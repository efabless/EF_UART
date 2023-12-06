import cocotb
from cocotb.triggers import Timer, RisingEdge, ClockCycles, FallingEdge, NextTimeStep, Edge
from collections import namedtuple
from caravel_cocotb.ips_models import EF_apbModel
from UART_monitor import UART_apbMonitor
from cocotb.queue import Queue
import os
import tabulate
from tabulate import tabulate
from UART_Coverage import UART_Coverage

UART_Transaction = namedtuple("UART_Transaction", ["type", "char"])


class UART_apbModel(EF_apbModel):
    def __init__(self, hdl, ip_name="UART", cov_hierarchy="uart", coverage_enabled=False, logging_enabled=False):
        json_file = os.path.join(os.path.dirname(__file__), "../../../EF_UART.json")
        super().__init__(hdl, json_file, ip_name, cov_hierarchy, coverage_enabled, logging_enabled)
        uart_queue = Queue()

        UART_apbMonitor(hdl, uart_queue, self.ip_regs.get_regs())
        UartModel(uart_queue, self.ip_regs, ip_name, cov_hierarchy, coverage_enabled, logging_enabled)


class UartModel():
    def __init__(self, queue, ip_regs, ip_name, cov_hierarchy="uart_ip", coverage_enabled=False, logging_enabled=False) -> None:
        self.ip_regs = ip_regs
        self.ip_regs_dict = ip_regs.get_regs()
        self.coverge_enabled = coverage_enabled
        self.logging_enabled = logging_enabled
        if self.logging_enabled:
            self.configure_logger(logger_file=f"{ip_name}.log")
        self._thread = cocotb.scheduler.add(self._model(queue))
        if self.coverge_enabled:
            self.cov = UART_Coverage(cov_hierarchy)

    async def _model(self, queue):
        while True:
            transaction = await self._get_transactions(queue)
            cocotb.log.debug(f"[{__class__.__name__}][_model] {transaction}")
            if self.logging_enabled:
                self.log_operation(transaction)
            if self.coverge_enabled:
                self.sample_coverage(transaction)

    def sample_coverage(self, transaction):
        self.cov.uart_cov(transaction)

    async def _get_transactions(self, queue):
        transaction = await queue.get()
        cocotb.log.debug(f"[{__class__.__name__}][_get_transactions] getting transaction {transaction} from monitor type {type(transaction)}")
        return transaction

    def configure_logger(self, logger_file="log.txt"):
        if not os.path.exists("loggers"):
            os.makedirs("loggers")
        self.logger_file = f"{os.getcwd()}/loggers/{logger_file}"
        # # log the header
        self.log_operation(None, header_logged=True)

    def log_operation(self, transaction, header_logged=False):
        if header_logged:
            # Log the header
            pass
            header = tabulate([], headers=["Time", "Type", "Char", "prescale"], tablefmt="grid")
            with open(self.logger_file, 'w') as f:
                f.write(f"{header}\n")
        else:
            table_data = [(
                f"{cocotb.utils.get_sim_time(units='ns')} ns",
                f"{transaction.type}",
                f"{transaction.char}",
                f"{transaction.prescale}"
                )]
            table = tabulate(table_data, tablefmt="grid")
            with open(self.logger_file, 'a') as f:
                f.write(f"{table}\n")

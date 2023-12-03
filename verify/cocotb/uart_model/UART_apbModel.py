import cocotb
from cocotb.triggers import Timer, RisingEdge, ClockCycles, FallingEdge, NextTimeStep, Edge
from collections import namedtuple
from caravel_cocotb.ips_models import EF_apbModel
import os

UART_Transaction = namedtuple("UART_Transaction", ["type", "char"])


class UART_apbModel(EF_apbModel):
    def __init__(self, hdl, ip_name="UART", cov_hierarchy="uart", coverage_enabled=False, logging_enabled=False):
        json_file = os.path.join(os.path.dirname(__file__), "../../../EF_UART.json")
        super().__init__(hdl, json_file, ip_name, cov_hierarchy, coverage_enabled, logging_enabled)

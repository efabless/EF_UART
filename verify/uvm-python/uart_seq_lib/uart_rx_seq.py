from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_info, uvm_fatal
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from uvm.base import sv, UVM_HIGH, UVM_LOW
from uart_item.uart_item import uart_item
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb_coverage.coverage import coverage_db
import os
import random
from uart_seq_lib.uart_config import uart_config


class uart_rx_seq(UVMSequence):

    def __init__(self, name="uart_rx_seq"):
        UVMSequence.__init__(self, name)
        self.set_automatic_phase_objection(1)
        self.req = uart_item()
        self.rsp = uart_item()
        self.tag = name

    async def body(self):
        # configure uart
        for _ in range(18):
            await uvm_do_with(self, self.req, lambda direction: direction == uart_item.RX)


uvm_object_utils(uart_rx_seq)

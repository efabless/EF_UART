from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_info, uvm_fatal
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from uvm.base import sv, UVM_HIGH, UVM_LOW
from EF_UVM.bus_env.bus_item import bus_bus_item
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb_coverage.coverage import coverage_db
import os
import random
from uart_seq_lib.uart_config import uart_config
from EF_UVM.bus_env.bus_seq_lib.reset_seq import reset_seq
class uart_tx_seq(UVMSequence):

    def __init__(self, name="uart_tx_seq"):
        UVMSequence.__init__(self, name)
        self.set_automatic_phase_objection(1)
        self.req = bus_bus_item()
        self.rsp = bus_bus_item()
        self.tag = name

    async def body(self):
        # configure uart 
        config_seq = uart_config("uart_config")
        await uvm_do(self, config_seq)  # change the presclar
        for _ in range(30):
            random_send = random.randint(1, 16)
            for __ in range(random_send):
                await uvm_do_with(self, self.req, lambda addr: addr == 0x4, lambda kind: kind == bus_bus_item.WRITE, lambda data: data in range(0, 0x200))
            for __ in range(random.randint(0, random_send-1 if random_send > 1 else 1)):
                await self.monitor.tx_received.wait()
                self.monitor.tx_received.clear()


uvm_object_utils(uart_tx_seq)

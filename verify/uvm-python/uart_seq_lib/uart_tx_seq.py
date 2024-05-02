from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_info, uvm_fatal
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from uvm.base import sv, UVM_HIGH, UVM_LOW
from EF_UVM.bus_env.bus_item import bus_item
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb_coverage.coverage import coverage_db
import os
import random
from uart_seq_lib.uart_config import uart_config
from EF_UVM.bus_env.bus_seq_lib.bus_seq_base import bus_seq_base


class uart_tx_seq(bus_seq_base):

    def __init__(self, name="uart_tx_seq"):
        super().__init__(name)
        self.tag = name

    async def body(self):
        # configure uart
        config_seq = uart_config("uart_config")
        self.create_new_item()
        await uvm_do(self, config_seq)  # change the presclar
        for _ in range(30):
            random_send = random.randint(1, 16)
            for __ in range(random_send):
                self.create_new_item()
                await uvm_do_with(
                    self,
                    self.req,
                    lambda addr: addr == 0x4,
                    lambda kind: kind == bus_item.WRITE,
                    lambda data: data in range(0, 0x200),
                )
            for __ in range(
                random.randint(0, random_send - 1 if random_send > 1 else 1)
            ):
                await self.monitor.tx_received.wait()
                self.monitor.tx_received.clear()


uvm_object_utils(uart_tx_seq)

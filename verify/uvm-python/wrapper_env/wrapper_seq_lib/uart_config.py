from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_info, uvm_fatal
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from uvm.base import sv, UVM_HIGH, UVM_LOW
from wrapper_env.wrapper_item import wrapper_bus_item
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb_coverage.coverage import coverage_db
import os
import random
from wrapper_env.wrapper_seq_lib.seq_base import seq_base

class uart_config(seq_base):

    def __init__(self, name="uart_config"):
        super().__init__(name)

    async def body(self):
        await super().body()
        # get register names/address conversion dict
        
        # randomly config uart
        # first disabled the uart
        await uvm_do_with(self, self.req, lambda addr: addr == self.adress_dict["control"], lambda kind: kind == wrapper_bus_item.WRITE, lambda data: data == 0)

        # random prescale value
        await uvm_do_with(self, self.req, lambda addr: addr == self.adress_dict["prescaler"], lambda kind: kind == wrapper_bus_item.WRITE, lambda data: data in range(0, 0x10))

        # random config
        await uvm_do_with(self, self.req, lambda addr: addr == self.adress_dict["config"], lambda kind: kind == wrapper_bus_item.WRITE, lambda data: (data>>8) == 0x3f and (data&0xf) in range(5, 10) and ((data&0xE0) >> 5) in [0,1,2,4,5] and data&0xF ==9)

        # random IM 
        await uvm_do_with(self, self.req, lambda addr: addr == self.adress_dict["im"], lambda kind: kind == wrapper_bus_item.WRITE)

        # enable uart
        await uvm_do_with(self, self.req, lambda addr: addr == self.adress_dict["control"], lambda kind: kind == wrapper_bus_item.WRITE, lambda data: data == 0x17)


uvm_object_utils(uart_config)

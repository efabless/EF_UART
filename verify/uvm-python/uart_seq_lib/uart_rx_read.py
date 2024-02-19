from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_info, uvm_fatal
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from uvm.base import sv, UVM_HIGH, UVM_LOW
from EF_UVM.wrapper_env.wrapper_item import wrapper_bus_item
from uvm.base.uvm_config_db import UVMConfigDb
import random


class uart_rx_read(UVMSequence):

    def __init__(self, name="uart_rx_read"):
        UVMSequence.__init__(self, name)
        self.set_automatic_phase_objection(1)
        self.req = wrapper_bus_item()
        self.rsp = wrapper_bus_item()
        self.tag = name

    async def body(self):
        # get register names/address conversion dict
        arr = []
        if (not UVMConfigDb.get(self, "", "wrapper_regs", arr)):
            uvm_fatal(self.tag, "No json file wrapper regs")
        else:
            adress_dict = arr[0].reg_name_to_address
        # randomly config uart
        # first disabled the uart
        for _ in range(random.randint(1, 18)):
            await uvm_do_with(self, self.req, lambda addr: addr == adress_dict["RXDATA"], lambda kind: kind == wrapper_bus_item.READ, lambda data: data == 0)
            # await uvm_do_with(self, self.req, lambda addr: addr == adress_dict["im"], lambda kind: kind == wrapper_bus_item.WRITE, lambda data: data == 0)


uvm_object_utils(uart_rx_read)

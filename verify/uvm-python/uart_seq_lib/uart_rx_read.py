from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_info, uvm_fatal
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from uvm.base import sv, UVM_HIGH, UVM_LOW
from EF_UVM.bus_env.bus_item import bus_item
from uvm.base.uvm_config_db import UVMConfigDb
import random
from EF_UVM.bus_env.bus_seq_lib.bus_seq_base import bus_seq_base


class uart_rx_read(bus_seq_base):

    def __init__(self, name="uart_rx_read"):
        super().__init__(name)
        self.tag = name

    async def body(self):
        # get register names/address conversion dict
        arr = []
        if not UVMConfigDb.get(self, "", "bus_regs", arr):
            uvm_fatal(self.tag, "No json file wrapper regs")
        else:
            adress_dict = arr[0].reg_name_to_address
        # randomly config uart
        # first disabled the uart
        for _ in range(random.randint(1, 18)):
            await uvm_do_with(
                self,
                self.req,
                lambda addr: addr == adress_dict["RXDATA"],
                lambda kind: kind == bus_item.READ,
                lambda data: data == 0,
            )
            # await uvm_do_with(self, self.req, lambda addr: addr == adress_dict["im"], lambda kind: kind == bus_item.WRITE, lambda data: data == 0)


uvm_object_utils(uart_rx_read)

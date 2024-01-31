from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_sequence_defines import uvm_do_with
from uvm.base import sv, UVM_HIGH, UVM_LOW
from wrapper_env.wrapper_item import wrapper_bus_item
import random
from wrapper_env.wrapper_seq_lib.seq_base import seq_base
from uvm.macros.uvm_message_defines import uvm_info, uvm_fatal
from ip_env.ip_item import ip_item
from uvm.seq import UVMSequence

class rx_seq(UVMSequence):
    def __init__(self, name="tx_seq", repeat=3):
        UVMSequence.__init__(self, name)
        self.set_automatic_phase_objection(1)
        self.req = ip_item()
        self.rsp = ip_item()
        self.tag = name
        self.repeat = repeat

    async def body(self):
        # configure uart
        for _ in range(self.repeat):
            await uvm_do_with(self, self.req, lambda direction: direction == ip_item.RX)



uvm_object_utils(rx_seq)

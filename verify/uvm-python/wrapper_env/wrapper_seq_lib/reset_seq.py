from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_info, uvm_fatal
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from uvm.base import UVM_LOW
from ip_env.ip_seq_lib.seq_base import seq_base


class reset_seq(seq_base):
    def __init__(self, name="reset_seq"):
        super().__init__(name)

    async def body(self):
        uvm_info("self", "Resetting DUT", UVM_LOW)
        self.req.reset = 1
        await uvm_do(self, self.req)


uvm_object_utils(reset_seq)

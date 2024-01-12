
from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_info
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from uvm.base import sv, UVM_HIGH, UVM_LOW
from wrapper_env.wrapper_item import wrapper_bus_item

class write_seq(UVMSequence):

    def __init__(self, name="write_seq"):
        UVMSequence.__init__(self, name)
        self.set_automatic_phase_objection(1)
        self.req = wrapper_bus_item()
        self.rsp = wrapper_bus_item()
        
    async def body(self):
        self.req.kind = wrapper_bus_item.WRITE
        self.req.addr = 0
        self.req.data = 1
        # await uvm_do_with(self, self.req, lambda kind: kind == wrapper_bus_item.WRITE, lambda data: data in [0, 0xFF])
        await uvm_do_with(self, self.req, lambda addr: addr == 0xf08, lambda kind: kind == wrapper_bus_item.WRITE, lambda data: data==1)
        await uvm_do_with(self, self.req, lambda : True)
        await uvm_do(self, self.req)
        # rsp = []
        # await self.get_response(rsp)
        # self.rsp = rsp[0]
        # uvm_info("write_seq", "Got response: " + self.rsp.convert2string(), UVM_LOW)

uvm_object_utils(write_seq)

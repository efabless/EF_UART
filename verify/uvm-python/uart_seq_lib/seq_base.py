from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_fatal,uvm_info
from EF_UVM.bus_env.bus_item import bus_bus_item
from uvm.base.uvm_config_db import UVMConfigDb

from uvm.base.uvm_object_globals import UVM_FULL, UVM_LOW, UVM_ERROR

class seq_base(UVMSequence):

    def __init__(self, name="seq_base"):
        UVMSequence.__init__(self, name)
        self.set_automatic_phase_objection(1)
        self.req = bus_bus_item()
        self.rsp = bus_bus_item()
        self.tag = name

    async def body(self):
        # get register names/address conversion dict
        arr = []
        if (not UVMConfigDb.get(self, "", "bus_regs", arr)):
            uvm_fatal(self.tag, "No json file wrapper regs")
        else:
            self.adress_dict = arr[0].reg_name_to_address


uvm_object_utils(seq_base)

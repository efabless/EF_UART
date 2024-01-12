from uvm.seq.uvm_sequence_item import UVMSequenceItem
from uvm.macros import uvm_object_utils_begin, uvm_object_utils_end, uvm_field_int, uvm_object_utils
from uvm.base.uvm_object_globals import UVM_ALL_ON, UVM_NOPACK
from uvm.base.sv import sv


class ip_item(UVMSequenceItem):

    def __init__(self, name="ip_item"):
        super().__init__(name)
        self.char = 0  # bit
        self.rand("char", range(0, 0x8F))
        pass

    def convert2string(self):
        return sv.sformatf("uart char=%s", self.char)


uvm_object_utils(ip_item)

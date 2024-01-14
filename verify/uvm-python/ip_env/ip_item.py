from uvm.seq.uvm_sequence_item import UVMSequenceItem
from uvm.macros import uvm_object_utils_begin, uvm_object_utils_end, uvm_field_int, uvm_object_utils
from uvm.base.uvm_object_globals import UVM_ALL_ON, UVM_NOPACK
from uvm.base.sv import sv


class ip_item(UVMSequenceItem):

    RX = 0
    TX = 1
    def __init__(self, name="ip_item"):
        super().__init__(name)
        self.char = 0  # bit
        self.rand("char", range(0, 0x80))
        self._direction = None
        self.direction = ip_item.RX
        pass

    def convert2string(self):
        dirct = "RX" if self.direction == ip_item.RX else "TX"
        return sv.sformatf("uart char=%s direction=%s", self.char, dirct)

    def do_compare(self, tr):
        return self.char == tr.char and self.direction == tr.direction

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if value in [ip_item.RX, ip_item.TX]:
            self._direction = value
        else:
            raise ValueError("direction must be RX or TX")


uvm_object_utils(ip_item)

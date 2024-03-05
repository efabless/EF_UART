from uvm.seq.uvm_sequence_item import UVMSequenceItem
from uvm.macros import uvm_object_utils_begin, uvm_object_utils_end, uvm_field_int, uvm_object_utils, uvm_error, uvm_info
from uvm.base.uvm_object_globals import UVM_ALL_ON, UVM_NOPACK, UVM_HIGH, UVM_MEDIUM
from uvm.base.sv import sv
from EF_UVM.ip_env.ip_item import ip_item

class uart_item(ip_item):

    RX = 0
    TX = 1
    def __init__(self, name="uart_item"):
        super().__init__(name)
        self.char = 0  # bit
        self.rand("char", range(0, 0x1FF))
        self.tag = name
        self._direction = None
        self.direction = uart_item.RX
        self.word_length = 8
        self.parity= "None"
        pass

    def convert2string(self):
        dirct = "RX" if self.direction == uart_item.RX else "TX"
        return sv.sformatf("uart char=%s(0x%0h) direction=%s, word_length=%d, parity=%s", chr(self.char), self.char,dirct, self.word_length, self.parity)

    def do_compare(self, tr):
        uvm_info(self.tag, "Comparing " + self.convert2string() + " with " + tr.convert2string(), UVM_MEDIUM)
        return self.char == tr.char and self.direction == tr.direction 

    def calculate_parity(self, parity_type):
        # uvm_info(self.tag, "Parity type = " + str(parity_type), UVM_HIGH)
        if parity_type == 0:
            self.parity = "None"
        elif parity_type == 1:  # odd
            self.parity = "0" if self.count_ones(self.char) % 2 else "1"
        elif parity_type == 2:  # even
            self.parity =  "0" if self.count_ones(self.char) % 2 == 0 else "1"
        elif parity_type == 4:  # sticky 0
            self.parity = "0"
        elif parity_type == 5:  # sticky 1
            self.parity = "1"
        else:
            uvm_error(self.tag, "Parity has invalid value: " + str(parity_type))
            return "None"

    def count_ones(self, n):
        count = 0
        while n:
            count += n & 1  # Increment count if the least significant bit is 1
            n >>= 1  # Right shift to check the next bit
        return count

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if value in [uart_item.RX, uart_item.TX]:
            self._direction = value
        else:
            raise ValueError("direction must be RX or TX")


uvm_object_utils(uart_item)

from uvm.seq.uvm_sequence_item import UVMSequenceItem
from uvm.macros import (
    uvm_object_utils_begin,
    uvm_object_utils_end,
    uvm_field_int,
    uvm_object_utils,
    uvm_error,
)
from uvm.base.uvm_object_globals import UVM_ALL_ON, UVM_NOPACK
from uvm.base.sv import sv


class uart_interrupt(UVMSequenceItem):
    """item to communicate the interrupts that is calculated from from monitor to the vip"""

    def __init__(self, name="uart_interrupt"):
        super().__init__(name)
        self.rx_timeout = 0  # bit
        self.rx_break_line = 0  # bit
        self.rx_wrong_parity = 0  # bit
        self.rx_frame_error = 0  # bit
        pass

    def convert2string(self):
        return sv.sformatf(
            "rx_timeout = %d, rx_break_line = %d, rx_wrong_parity = %d, rx_frame_error = %d",
            self.rx_timeout,
            self.rx_break_line,
            self.rx_wrong_parity,
            self.rx_frame_error,
        )


uvm_object_utils(uart_interrupt)

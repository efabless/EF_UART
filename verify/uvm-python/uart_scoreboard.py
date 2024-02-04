from uvm.comps import UVMScoreboard
from uvm.macros import uvm_component_utils, uvm_info
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW
from uart_item.uart_item import uart_item
from EF_UVM.scoreboard import scoreboard

#  TODO: replace this with callback in the future


class uart_scoreboard(scoreboard):
    def __init__(self, name="scoreboard", parent=None):
        super().__init__(name, parent)
        pass

    def write_ip(self, tr):
        # filter the ip checker to check only the TX, RX ones are checked by reading the register
        uvm_info(self.tag, "write_ip: " + tr.convert2string(), UVM_MEDIUM)
        if tr.direction == uart_item.TX:
            self.q_ip.put_nowait(tr)


uvm_component_utils(uart_scoreboard)

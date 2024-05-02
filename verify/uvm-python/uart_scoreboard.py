from uvm.comps import UVMScoreboard
from uvm.macros import uvm_component_utils, uvm_info
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW
from uart_item.uart_item import uart_item
from EF_UVM.scoreboard import scoreboard
from uvm.macros import uvm_component_utils, uvm_info, uvm_error

#  TODO: replace this with callback in the future


class uart_scoreboard(scoreboard):
    def __init__(self, name="uart_scoreboard", parent=None):
        super().__init__(name, parent)

    def write_ip(self, tr):
        # filter the ip checker to check only the TX, RX ones are checked by reading the register
        uvm_info(self.tag, "write_ip: " + tr.convert2string(), UVM_HIGH)
        if tr.direction == uart_item.TX:
            self.q_ip.put_nowait(tr)

    def extract_phase(self, phase):
        # check all the quese is empty or at least has the same item
        if self.q_bus.qsize() not in [0, 1] or self.q_bus_ref_model.qsize() not in [
            0,
            1,
        ]:
            uvm_error(
                self.tag,
                f"Bus queue still have unchecked items queue bus {self.q_bus._queue} size {self.q_bus.qsize()} bus_ref_model {self.q_bus_ref_model._queue} size {self.q_bus_ref_model.qsize()}",
            )
        if self.q_irq.qsize() not in [0, 1] or self.q_irq_ref_model.qsize() not in [
            0,
            1,
        ]:
            uvm_error(
                self.tag,
                f"IRQ queue still have unchecked items queue irq {self.q_irq._queue} size {self.q_irq.qsize()} irq_ref_model {self.q_irq_ref_model._queue} size {self.q_irq_ref_model.qsize()}",
            )
        if self.q_ip.qsize() not in [0, 1] or self.q_ip_ref_model.qsize() not in [0, 1]:
            uvm_error(
                self.tag,
                f"IP queue still have unchecked items queue ip {self.q_ip._queue} size {self.q_ip.qsize()} ip_ref_model {self.q_ip_ref_model._queue} size {self.q_ip_ref_model.qsize()}",
            )


uvm_component_utils(uart_scoreboard)

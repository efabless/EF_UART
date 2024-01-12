from uvm.seq.uvm_sequencer import UVMSequencer
from uvm.macros import uvm_component_utils


class ip_sequencer(UVMSequencer):  # (apb_rw)

    def __init__(self, name, parent=None):
        super().__init__(name, parent)


uvm_component_utils(ip_sequencer)
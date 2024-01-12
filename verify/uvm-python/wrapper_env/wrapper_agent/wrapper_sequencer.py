from uvm.seq.uvm_sequencer import UVMSequencer
from uvm.macros import uvm_component_utils


class wrapper_sequencer(UVMSequencer):

    def __init__(self, name, parent=None):
        super().__init__(name, parent)


uvm_component_utils(wrapper_sequencer)
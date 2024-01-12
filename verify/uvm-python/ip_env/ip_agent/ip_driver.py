from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.comps.uvm_driver import UVMDriver
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb.triggers import Timer, RisingEdge
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW
from ip_env.ip_item import ip_item


class ip_driver(UVMDriver):
    def __init__(self, name="ip_driver", parent=None):
        super().__init__(name, parent)
        self.tag = name

    def build_phase(self, phase):
        super().build_phase(phase)
        arr = []
        if (not UVMConfigDb.get(self, "", "ip_if", arr)):
            uvm_fatal(self.tag, "No interface specified for self driver instance")
        else:
            self.sigs = arr[0]

    async def run_phase(self, phase):
        uvm_info(self.tag, "run_phase started", UVM_LOW)
        pass


uvm_component_utils(ip_driver)

from uvm.comps.uvm_agent import UVMAgent
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from wrapper_env.wrapper_agent.wrapper_sequencer import wrapper_sequencer
from wrapper_env.wrapper_agent.wrapper_driver import wrapper_driver
from wrapper_env.wrapper_agent.wrapper_bus_monitor import wrapper_bus_monitor
from wrapper_env.wrapper_agent.wrapper_irq_monitor import wrapper_irq_monitor
from uvm.tlm1.uvm_analysis_port import UVMAnalysisExport
from uvm.base.uvm_config_db import UVMConfigDb


class wrapper_agent(UVMAgent):
    def __init__(self, name="wrapper_agent", parent=None):
        super().__init__(name, parent)
        self.tag = name
        self.wrapper_sequencer = None
        self.driver = None
        self.bus_monitor = None
        self.irq_monitor = None
        self.agent_bus_export = UVMAnalysisExport("agent_bus_export", self)
        self.agent_irq_export = UVMAnalysisExport("agent_irq_export", self)

    def build_phase(self, phase):
        self.wrapper_sequencer = wrapper_sequencer.type_id.create("wrapper_sequencer", self)
        self.driver = wrapper_driver.type_id.create("wrapper_driver", self)
        self.bus_monitor = wrapper_bus_monitor.type_id.create("wrapper_bus_monitor", self)
        arr = []
        if (not UVMConfigDb.get(self, "", "irq_exist", arr)):
            uvm_fatal(self.tag, "No info about irq exists in config DB")
        else:
            irq_exist = arr[0]
        if irq_exist:
            self.irq_monitor = wrapper_irq_monitor.type_id.create("wrapper_irq_monitor", self)

    def connect_phase(self, phase):
        self.driver.seq_item_port.connect(self.wrapper_sequencer.seq_item_export)
        self.bus_monitor.monitor_port.connect(self.agent_bus_export)
        self.irq_monitor.monitor_port.connect(self.agent_irq_export)
        pass


uvm_component_utils(wrapper_agent)

from uvm.comps.uvm_agent import UVMAgent
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from ip_env.ip_agent.ip_sequencer import ip_sequencer
from ip_env.ip_agent.ip_driver import ip_driver
from ip_env.ip_agent.ip_monitor import ip_monitor
from uvm.tlm1.uvm_analysis_port import UVMAnalysisExport
from uvm.base.uvm_config_db import UVMConfigDb


class ip_agent(UVMAgent):
    def __init__(self, name="ip_agent", parent=None):
        super().__init__(name, parent)
        self.tag = name
        self.ip_sequencer = None
        self.driver = None
        self.monitor = None
        self.agent_export = UVMAnalysisExport("agent_export", self)

    def build_phase(self, phase):
        self.ip_sequencer = ip_sequencer.type_id.create("ip_sequencer", self)
        self.driver = ip_driver.type_id.create("ip_driver", self)
        self.monitor = ip_monitor.type_id.create("ip_monitor", self)

    def connect_phase(self, phase):
        self.driver.seq_item_port.connect(self.ip_sequencer.seq_item_export)
        self.monitor.monitor_port.connect(self.agent_export)
        pass


uvm_component_utils(ip_agent)

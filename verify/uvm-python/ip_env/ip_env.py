from uvm.comps import UVMEnv
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from ip_env.ip_agent.ip_agent import ip_agent
from ip_env.ip_coverage.ip_coverage import ip_coverage
from ip_env.ip_logger.ip_logger import ip_logger
from uvm.tlm1.uvm_analysis_port import UVMAnalysisExport


class ip_env(UVMEnv):
    """
    The ipEnv is a dedicated environment designed for the thorough verification of the IP (Intellectual Property).The ipEnv comprises several key components:

        Agent: Central to the ipEnv is the agent, which encompasses both a driver and a monitor.
        Coverage Model:It analyzes the information gathered by the monitor to evaluate the depth and breadth of the test coverage.
        The coverage model helps in identifying functional aspects of the IP that have not been adequately tested, guiding the development of additional tests to cover these areas.
        Logger Model:It systematically logs the operations, transactions, and interactions of the IP as observed by the monitor.
        These logs are formatted into tables, providing a clear and chronological record of the IP's behavior.
        This detailed logging is invaluable for debugging and pinpointing specific issues in the IP's functionality.
    """
    def __init__(self, name="ip_env", parent=None):
        super().__init__(name, parent)
        self.coverage_comp = None
        self.logger_comp = None
        self.ip_agent = None
        self.ip_env_export = UVMAnalysisExport("ip_env_export", self)

    def build_phase(self, phase):
        self.ip_agent = ip_agent.type_id.create("ip_agent", self)
        self.coverage_comp = ip_coverage.type_id.create("ip_coverage", self)
        self.logger_comp = ip_logger.type_id.create("ip_logger", self)
        pass

    def connect_phase(self, phase):
        self.ip_agent.agent_export.connect(self.ip_env_export)
        self.ip_agent.agent_export.connect(self.coverage_comp.analysis_imp)
        self.ip_agent.agent_export.connect(self.logger_comp.analysis_imp)
        pass


uvm_component_utils(ip_env)

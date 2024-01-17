from uvm.comps import UVMEnv
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from wrapper_env.wrapper_agent.wrapper_agent import wrapper_agent
from wrapper_env.wrapper_coverage.wrapper_coverage import wrapper_coverage
from wrapper_env.wrapper_logger.wrapper_logger import wrapper_logger
from uvm.tlm1.uvm_analysis_port import UVMAnalysisExport


class wrapper_env(UVMEnv):
    """
        The wrapperEnv is a specialized environment for verifying the bus system in an IP (Intellectual Property) design. This environment is structured to ensure comprehensive testing and validation of the bus interface, which could be of various types such as Wishbone, AHB, or APB. Its three main components are:
            Agent: At the core of the wrapperEnv is the agent, which includes both a driver and a monitor.
            Coverage Model: This component is closely linked with the monitor. It analyzes the outputs captured by the monitor to measure the extent of the test coverage.
            Logger Model: The logger model works in conjunction with the monitor to log activities and events in the bus system.
            It captures detailed logs of the transactions and interactions observed by the monitor.
    """
    def __init__(self, name="wrapper_env", parent=None):
        super().__init__(name, parent)
        self.coverage_comp = None
        self.logger_comp = None
        self.wrapper_agent = None
        self.wrapper_bus_export = UVMAnalysisExport("wrapper_bus_export", self)
        self.wrapper_irq_export = UVMAnalysisExport("wrapper_irq_export", self)

    def build_phase(self, phase):
        self.wrapper_agent = wrapper_agent.type_id.create("wrapper_agent", self)
        self.coverage_comp = wrapper_coverage.type_id.create("wrapper_coverage", self)
        self.logger_comp = wrapper_logger.type_id.create("wrapper_logger", self)
        pass

    def connect_phase(self, phase):
        self.wrapper_agent.agent_bus_export.connect(self.wrapper_bus_export)
        self.wrapper_agent.agent_irq_export.connect(self.wrapper_irq_export)
        self.wrapper_agent.agent_bus_export.connect(self.coverage_comp.analysis_imp_bus)
        self.wrapper_agent.agent_irq_export.connect(self.coverage_comp.analysis_imp_irq)
        self.wrapper_agent.agent_bus_export.connect(self.logger_comp.analysis_imp_bus)
        pass


uvm_component_utils(wrapper_env)

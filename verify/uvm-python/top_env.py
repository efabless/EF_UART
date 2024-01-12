from uvm.comps import UVMEnv
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from ip_env.ip_env import ip_env
from wrapper_env.wrapper_env import wrapper_env
from vip.vip import vip
from scoreboard import scoreboard


class top_env(UVMEnv):
    def __init__(self, name="env", parent=None):
        super().__init__(name, parent)
        self.ip_env = None
        self.wrapper_env = None
        self.vip = None
        self.scoreboard = None

    def build_phase(self, phase):
        self.ip_env = ip_env.type_id.create("ip_env", self)
        self.wrapper_env = wrapper_env.type_id.create("wrapper_env", self)
        self.vip = vip.type_id.create("vip", self)
        self.scoreboard = scoreboard.type_id.create("scoreboard", self)

    def connect_phase(self, phase):
        self.wrapper_env.wrapper_bus_export.connect(self.vip.analysis_imp)
        # scoreboard connection
        self.wrapper_env.wrapper_bus_export.connect(self.scoreboard.analysis_imp_bus)
        self.wrapper_env.wrapper_irq_export.connect(self.scoreboard.analysis_imp_irq)
        self.ip_env.ip_env_export.connect(self.scoreboard.uvm_analysis_imp_ip)
        self.vip.wrapper_bus_export.connect(self.scoreboard.analysis_imp_bus_vip)
        self.vip.wrapper_irq_export.connect(self.scoreboard.analysis_imp_irq_vip)
        self.vip.ip_export.connect(self.scoreboard.uvm_analysis_imp_ip_vip)
        pass


uvm_component_utils(top_env)

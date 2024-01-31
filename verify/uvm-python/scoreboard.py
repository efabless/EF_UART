from uvm.comps import UVMScoreboard
from uvm.macros.uvm_tlm_defines import uvm_analysis_imp_decl
from uvm.macros import uvm_component_utils, uvm_info, uvm_error
from cocotb.queue import Queue
import cocotb
from wrapper_env.wrapper_item import wrapper_bus_item
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW
from ip_env.ip_item import ip_item


uvm_analysis_imp_bus = uvm_analysis_imp_decl("_bus")
uvm_analysis_imp_irq = uvm_analysis_imp_decl("_irq")
uvm_analysis_imp_ip = uvm_analysis_imp_decl("_ip")
uvm_analysis_imp_bus_vip = uvm_analysis_imp_decl("_bus_vip")
uvm_analysis_imp_irq_vip = uvm_analysis_imp_decl("_irq_vip")
uvm_analysis_imp_ip_vip = uvm_analysis_imp_decl("_ip_vip")


class scoreboard(UVMScoreboard):
    def __init__(self, name="scoreboard", parent=None):
        super().__init__(name, parent)
        self.analysis_imp_bus = uvm_analysis_imp_bus("analysis_imp_bus", self)
        self.analysis_imp_irq = uvm_analysis_imp_irq("analysis_imp_irq", self)
        self.uvm_analysis_imp_ip = uvm_analysis_imp_ip("analysis_imp_ip", self)
        self.analysis_imp_bus_vip = uvm_analysis_imp_bus_vip("analysis_imp_bus_vip", self)
        self.analysis_imp_irq_vip = uvm_analysis_imp_irq_vip("analysis_imp_irq_vip", self)
        self.uvm_analysis_imp_ip_vip = uvm_analysis_imp_ip_vip("analysis_imp_ip_vip", self)
        self.tag = name
        self.q_bus = Queue()
        self.q_bus_vip = Queue()
        self.q_irq = Queue()
        self.q_irq_vip = Queue()
        self.q_ip = Queue()
        self.q_ip_vip = Queue()
        cocotb.scheduler.add(self.checker_bus())
        cocotb.scheduler.add(self.checker_irq())
        cocotb.scheduler.add(self.checker_ip())

    def build_phase(self, phase):
        super().build_phase(phase)

    def connect_phase(self, phase):
        super().connect_phase(phase)

    def write_bus(self, tr):
        if tr.kind == wrapper_bus_item.READ:
            self.q_bus.put_nowait(tr)
            uvm_info(self.tag, "write_bus: " + tr.convert2string(), UVM_MEDIUM)

    def write_bus_vip(self, tr):
        if tr.kind == wrapper_bus_item.READ:
            self.q_bus_vip.put_nowait(tr)
            uvm_info(self.tag, "write_bus_vip: " + tr.convert2string(), UVM_MEDIUM)

    async def checker_bus(self):
        while True:
            val = await self.q_bus.get()
            exp = await self.q_bus_vip.get()
            if not val.do_compare(exp):
                uvm_error(self.tag, "Bus mismatch: " + val.convert2string() + " != " + exp.convert2string())

    def write_irq(self, tr):
        uvm_info(self.tag, "write_irq: " + tr.convert2string(), UVM_MEDIUM)
        self.q_irq.put_nowait(tr)

    def write_irq_vip(self, tr):
        uvm_info(self.tag, "write_irq_vip: " + tr.convert2string(), UVM_MEDIUM)
        self.q_irq_vip.put_nowait(tr)

    async def checker_irq(self):
        while True:
            val = await self.q_irq.get()
            exp = await self.q_irq_vip.get()
            if not val.do_compare(exp):
                uvm_error(self.tag, "IRQ mismatch: " + val.convert2string() + " != " + exp.convert2string())

    def write_ip(self, tr):
        uvm_info(self.tag, "write_ip: " + tr.convert2string(), UVM_MEDIUM)
        if tr.direction == ip_item.TX:
            self.q_ip.put_nowait(tr)

    def write_ip_vip(self, tr):
        uvm_info(self.tag, "write_ip_vip: " + tr.convert2string(), UVM_MEDIUM)
        self.q_ip_vip.put_nowait(tr)

    async def checker_ip(self):
        while True:
            val = await self.q_ip.get()
            exp = await self.q_ip_vip.get()
            if not val.do_compare(exp):
                uvm_error(self.tag, "IP mismatch: " + val.convert2string() + " != " + exp.convert2string())

    def extract_phase(self, phase):
        super().extract_phase(phase)
        # check all the quese is empty or at least has the same item
        if self.q_bus.qsize() not in [0, 1] or  self.q_bus_vip.qsize() not in [0, 1]:
            uvm_error(self.tag, f"Bus queue still have unchecked items queue bus {self.q_bus._queue} size {self.q_bus.qsize()} bus_vip {self.q_bus_vip._queue} size {self.q_bus_vip.qsize()}")
        if self.q_irq.qsize() not in [0, 1] or self.q_irq_vip.qsize() not in [0, 1]:
            uvm_error(self.tag, f"IRQ queue still have unchecked items queue irq {self.q_irq._queue} size {self.q_irq.qsize()} irq_vip {self.q_irq_vip._queue} size {self.q_irq_vip.qsize()}")
        if self.q_ip.qsize() not in [0, 1] or self.q_ip_vip.qsize() not in [0, 1]:
            uvm_error(self.tag, f"IP queue still have unchecked items queue ip {self.q_ip._queue} size {self.q_ip.qsize()} ip_vip {self.q_ip_vip._queue} size {self.q_ip_vip.qsize()}")


uvm_component_utils(scoreboard)

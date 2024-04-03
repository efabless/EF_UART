from uvm.base.uvm_component import UVMComponent
from uvm.macros import uvm_component_utils
from uvm.tlm1.uvm_analysis_port import UVMAnalysisImp
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW, UVM_MEDIUM 
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_config_db import UVMConfigDb
from ref_model.model import EF_UART
from EF_UVM.bus_env.bus_item import bus_item, bus_irq_item
from uvm.tlm1.uvm_analysis_port import UVMAnalysisExport
from uvm.macros.uvm_tlm_defines import uvm_analysis_imp_decl
from uart_item.uart_item import uart_item
import cocotb
from EF_UVM.ref_model.ref_model import ref_model 



class UART_VIP(ref_model):
    """
    The VIP, or Verification IP, is a crucial element within the top-level verification environment, designed to validate the functionality and performance of both the IP (Intellectual Property) and the bus system. Its primary role is to act as a representative or mimic of the actual hardware components, including the IP and the bus. Key features and functions of the VIP include:
    1) Input Simulation: The VIP is capable of receiving the same inputs that would be provided to the actual IP and bus via connection with the monitors of the bus and IP.
    2) Functional Emulation: It emulates the behavior and responses of the IP and bus under test. By replicating the operational characteristics of these components, the VIP serves as a benchmark for expected performance and behavior.
    3) Output Generation: Upon receiving inputs, the VIP processes them in a manner akin to the real hardware, subsequently generating expected outputs. These outputs are essential for comparison in the verification process.
    4) Interface with Scoreboard: The outputs from the VIP, representing the expected results, are forwarded to the scoreboard. The scoreboard then compares these expected results with the actual outputs from the IP and bus for verification.
    5)Register Abstraction Layer (RAL) Integration: The VIP includes a RAL model that mirrors the register values of the RTL, ensuring synchronization between expected and actual register states. This model facilitates register-level tests and error detection, offering accessible and up-to-date register values for other verification components. It enhances the automation and coverage of register testing, playing a vital role in ensuring the accuracy and comprehensiveness of the verification process.
    """
    def __init__(self, name="ip_coverage", parent=None):
        super().__init__(name, parent)
        self.vip_model_rx_export = UVMAnalysisExport("vip_model_rx_export", self)

    def build_phase(self, phase):
        super().build_phase(phase)
        self.model = EF_UART.type_id.create("model", self)

    def start_of_simulation_phase(self, phase):
        cocotb.scheduler.add(self.update_irq())

    def connect_phase(self, phase):
        super().connect_phase(phase)
        self.model.ip_export.connect(self.ip_export)
        self.vip_model_rx_export.connect(self.model.analysis_imp_rx)

    def write_bus(self, tr):
        uvm_info(self.tag, "Vip write: " + tr.convert2string(), UVM_MEDIUM)
        if tr.kind == bus_item.RESET:
            self.model.reset()
            self.bus_bus_export.write(tr)
            return
        if tr.kind == bus_item.WRITE:
            self.model.write_register(tr.addr, tr.data)
            self.bus_bus_export.write(tr)
        elif tr.kind == bus_item.READ:
            uvm_info(self.tag, "Vip read: " + tr.convert2string(), UVM_MEDIUM)
            data = self.model.read_register(tr.addr)
            td = tr.do_clone()
            td.data = data
            self.bus_bus_export.write(td)

    def write_ip(self, tr):
        uvm_info(self.tag, "ip Vip write: " + tr.convert2string(), UVM_HIGH)
        if tr.direction == uart_item.TX:
            self.model.tx_trig_event.set()
        else:
            uvm_info(self.tag, "VIP receieved RX", UVM_HIGH)
            self.vip_model_rx_export.write(tr)

    def write_ip_irq(self, tr):
        uvm_info(self.tag, "ip_irq Vip write: " + tr.convert2string(), UVM_MEDIUM)
        if tr.rx_timeout:
            self.model.flags.set_timeout_err()
        if tr.rx_break_line:
            self.model.flags.set_line_break()
        if tr.rx_wrong_parity:
            self.model.flags.set_parity_err()
        if tr.rx_frame_error:
            self.model.flags.set_frame_err()

    async def update_irq(self):
        irq = 0
        while (True):
            await self.model.flags.mis_changed.wait()
            uvm_info(self.tag, f"mis changed mis = {self.model.regs.read_reg_value('mis')} irq = {irq}", UVM_MEDIUM)
            if self.model.regs.read_reg_value("mis") != 0 and irq == 0:
                irq = 1
                tr = bus_irq_item.type_id.create("tr", self)
                tr.trg_irq = 1
                self.bus_irq_export.write(tr)
            elif self.model.regs.read_reg_value("mis") == 0 and irq == 1:
                irq = 0
                tr = bus_irq_item.type_id.create("tr", self)
                tr.trg_irq = 0
                self.bus_irq_export.write(tr)
            self.model.flags.mis_changed.clear()


uvm_component_utils(UART_VIP)

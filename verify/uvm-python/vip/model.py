import cocotb
from cocotb.triggers import Timer, Event
from cocotb.clock import Clock
from cocotb.binary import BinaryValue
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info, uvm_warning
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW
from cocotb.queue import Queue
import asyncio
from ip_env.ip_item import ip_item
from uvm.base.uvm_component import UVMComponent
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.tlm1.uvm_analysis_port import UVMAnalysisExport
from uvm.macros.uvm_tlm_defines import uvm_analysis_imp_decl

uvm_analysis_imp_rx = uvm_analysis_imp_decl("_rx")


class EF_UART(UVMComponent):
    """
    EF UART specific model. every ip should have it's unique model
    """
    def __init__(self, name="EF_UART_Model", parent=None):
        super().__init__(name, parent)
        self.analysis_imp_rx = uvm_analysis_imp_rx("model_rx", self)
        self.ip_export = UVMAnalysisExport("model_export", self)
        self.tag = name
        pass

    def build_phase(self, phase):
        super().build_phase(phase)
        uvm_info(self.tag, "Vip built", UVM_MEDIUM)
        arr = []
        if (not UVMConfigDb.get(self, "", "wrapper_regs", arr)):
            uvm_fatal(self.tag, "No json file wrapper regs")
        else:
            self.regs = arr[0]
        self.tag = "EF_UART_model"
        self.fifo_tx = Queue(maxsize=15)
        self.fifo_rx = Queue(maxsize=16)
        self.tx_thread = None
        self.rx_thread = None
        self.event_control = Event()
        self.tx_trig_event = Event() # fire when monitor detect new tx received to sync the fifos
        cocotb.scheduler.add(self.control_regs())

    def write_register(self, addr, data):
        uvm_info(self.tag, "Writing register " + hex(addr) + " with value " + hex(data), UVM_MEDIUM)
        self.regs.write_reg_value(addr, data)
        if addr == self.regs.reg_name_to_address["txdata"]:  # txdata
            try:
                self.fifo_tx.put_nowait(data)
                uvm_info(self.tag, f"value {hex(data)} written to tx fifo size = {self.fifo_tx.qsize()}", UVM_MEDIUM)
            except asyncio.QueueFull:
                uvm_warning(self.tag, f"writing to tx while fifo is full so ignore the value {hex(data)}")
        if addr == 0x8:  # control
            uvm_info(self.tag, "UART control reg set", UVM_MEDIUM)
            self.event_control.set()

    def read_register(self, addr):
        uvm_info(self.tag, "Reading register " + hex(addr), UVM_MEDIUM)
        if addr == 0x4:  # txdata write only
            return 0xDEADBEEF
        elif addr == self.regs.reg_name_to_address["rxdata"]:  # reading from rx data
            try:
                return self.fifo_rx.get_nowait()
            except asyncio.QueueEmpty:
                return "X" # x means the data is trash so the scoreboard should not check it
        elif addr == 0x20:  # txlevel
            uvm_info(self.tag, "TX level: " + str(self.fifo_tx.qsize()), UVM_MEDIUM)
            return self.fifo_tx.qsize()
        return self.regs.read_reg_value(addr)

    async def transmit(self):
        # this should be called only if uart is enabled
        while (True):
            data_tx = await self.fifo_tx.get()
            uvm_info(self.tag, f"Transmitting {chr(data_tx)}({hex(data_tx)})", UVM_MEDIUM)
            tr = ip_item.type_id.create("tr", self)
            tr.char = chr(data_tx)
            tr.direction = ip_item.TX
            self.ip_export.write(tr)
            await self.tx_trig_event.wait()
            self.tx_trig_event.clear()

    async def receive(self):
        while True:
            data_rx = await self.fifo_rx.get()
            self.rx_data_is_x = False
            self.regs.write_reg_value(0x0, data_rx)

    def write_rx(self, tr):
        # if rx is enabled 
        if (self.regs.read_reg_value("control") & 7) in [5, 7]:
            try:
                self.fifo_rx.put_nowait(tr.char)
            except asyncio.QueueFull:
                uvm_warning(self.tag, "writing to rx while fifo is full so ignore the value")
        else:
            uvm_warning(self.tag, "received uart transaction while uart is disabled", UVM_MEDIUM)

    async def control_regs(self):
        while True:
            if (self.regs.read_reg_value("control") & 7) in [3, 7]:
                uvm_info(self.tag, "Enabling UART TX", UVM_MEDIUM)
                if self.tx_thread is None:
                    self.tx_thread = await cocotb.start(self.transmit())
            elif self.tx_thread is not None:
                uvm_info(self.tag, "Disabling UART TX", UVM_MEDIUM)
                self.tx_thread.kill()
                self.tx_thread = None

            uvm_info(self.tag, "UART control reg wait", UVM_MEDIUM)
            await self.event_control.wait()
            uvm_info(self.tag, "UART control reg changed", UVM_MEDIUM)
            self.event_control.clear()


uvm_component_utils(EF_UART)

import cocotb
from cocotb.triggers import Timer, Event, First
from cocotb.clock import Clock
from cocotb.binary import BinaryValue
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info, uvm_warning, uvm_error
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW, UVM_MEDIUM
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
        uvm_info(self.tag, "Vip built", UVM_HIGH)
        arr = []
        if (not UVMConfigDb.get(self, "", "wrapper_regs", arr)):
            uvm_fatal(self.tag, "No json file wrapper regs")
        else:
            self.regs = arr[0]
        self.tag = "EF_UART_model"
        self.fifo_tx = TX_QUEUE(maxsize=16)
        self.fifo_tx_threshold = True
        self.fifo_rx = Queue(maxsize=16)
        self.fifo_rx_threshold = False
        self.tx_thread = None
        self.event_control = Event()
        self.tx_trig_event = Event()  # fire when monitor detect new tx received to sync the fifos
        self.new_rx_received = Event()
        cocotb.scheduler.add(self.control_regs())

    def write_register(self, addr, data):
        uvm_info(self.tag, "Writing register " + hex(addr) + " with value " + hex(data), UVM_HIGH)
        self.regs.write_reg_value(addr, data)
        if addr == self.regs.reg_name_to_address["txdata"]:  # txdata
            try:
                word_mask = (1 << (self.regs.read_reg_value("config") & 0xf)) -1
                self.fifo_tx.put_nowait(data & word_mask)
                uvm_info(self.tag, f"value {hex(data)} written to tx fifo size = {self.fifo_tx.qsize()}", UVM_MEDIUM)
                self.check_tx_level_threshold()
                if self.fifo_tx.full():
                        uvm_info(self.tag, f"[interrupt flag] tx fifo is full", UVM_MEDIUM)
            except asyncio.QueueFull:
                uvm_warning(self.tag, f"writing to tx while fifo is full so ignore the value {hex(data)}")
        if addr == 0x8:  # control
            uvm_info(self.tag, "UART control reg set", UVM_HIGH)
            self.event_control.set()

    def read_register(self, addr):
        uvm_info(self.tag, "Reading register " + hex(addr), UVM_HIGH)
        if addr == self.regs.reg_name_to_address["rxdata"]:  # reading from rx data
            try:
                data = self.fifo_rx.get_nowait()
                self.check_rx_level_threshold()
                return data
            except asyncio.QueueEmpty:
                return "X" # x means the data is trash so the scoreboard should not check it
        return self.regs.read_reg_value(addr)

    async def transmit(self):
        # this should be called only if uart is enabled
        while (True):
            data_tx = await self.fifo_tx.get_no_pop()
            self.check_tx_level_threshold()
            uvm_info(self.tag, f"Transmitting {chr(data_tx)}({hex(data_tx)}) fifo size = {self.fifo_tx.qsize()}", UVM_HIGH)
            tr = ip_item.type_id.create("tr", self)
            tr.char = data_tx
            tr.direction = ip_item.TX
            parity_type = (self.regs.read_reg_value("config") >> 5) & 0x7
            tr.calculate_parity(parity_type)
            tr.word_length = self.regs.read_reg_value("config") & 0xf
            self.ip_export.write(tr)
            await self.tx_trig_event.wait()
            self.tx_trig_event.clear()
            # pop last value from as it is sent
            # update rx fifo when loopback is enabled 
            await self.fifo_tx.get()
            
            if (self.regs.read_reg_value("control") & 0xF) == 0xF:
                try:
                    self.fifo_rx.put_nowait(data_tx)
                    self.check_receiver_match(data_tx)
                    self.check_rx_level_threshold()
                    if self.fifo_rx.full():
                        uvm_info(self.tag, f"[interrupt flag] rx fifo is full", UVM_MEDIUM)
                except asyncio.QueueFull:
                    self.check_receiver_match(data_tx)
                    uvm_warning(self.tag, "writing to rx while fifo is full so ignore the value")
                    uvm_info(self.tag, f"[interrupt flag] rx fifo is full", UVM_MEDIUM)

    def write_rx(self, tr):
        # if rx is enabled
        if (self.regs.read_reg_value("control") & 7) in [5, 7]:
            try:
                self.fifo_rx.put_nowait(tr.char)
                self.check_receiver_match(tr.char)
                self.check_rx_level_threshold()
                self.new_rx_received.set()
                if self.fifo_rx.full():
                    uvm_info(self.tag, "[interrupt flag] rx fifo is full", UVM_MEDIUM)
            except asyncio.QueueFull:
                self.new_rx_received.set()
                self.check_receiver_match(tr.char)
                uvm_warning(self.tag, "writing to rx while fifo is full so ignore the value")
                uvm_info(self.tag, f"[interrupt flag] overrun data has been received but the RX FIFO is full ", UVM_MEDIUM)
        else:
            uvm_warning(self.tag, "received uart transaction while uart is disabled")

    async def control_regs(self):
        while True:
            if (self.regs.read_reg_value("control") & 7) in [3, 7]:
                uvm_info(self.tag, "Enabling UART TX", UVM_HIGH)
                if self.tx_thread is None:
                    self.tx_thread = await cocotb.start(self.transmit())
            elif self.tx_thread is not None:
                uvm_info(self.tag, "Disabling UART TX", UVM_HIGH)
                self.tx_thread.kill()
                self.tx_thread = None

            uvm_info(self.tag, "UART control reg wait", UVM_HIGH)
            await self.event_control.wait()
            uvm_info(self.tag, "UART control reg changed", UVM_HIGH)
            self.event_control.clear()

    def check_receiver_match(self, new_char):
        match_reg = self.regs.read_reg_value("match")
        if new_char == match_reg:
            uvm_info(self.tag, f"[interrupt flag] Receiver data match {hex(new_char)}", UVM_MEDIUM)

    def check_rx_level_threshold(self):
        threshold = (self.regs.read_reg_value("fifo_control") >> 8) & 0b1111
        uvm_info(self.tag, f"RX threshold = {threshold} size = {self.fifo_rx.qsize()}", UVM_HIGH)
        if self.fifo_rx.qsize() > threshold:
            if not self.fifo_rx_threshold:
                self.fifo_rx_threshold = True
                uvm_info(self.tag, "[interrupt flag] Enabling RX FIFO thread", UVM_HIGH)
        else:
            if self.fifo_rx_threshold:
                self.fifo_rx_threshold = False
                uvm_info(self.tag, "[interrupt flag] Disabling RX FIFO thread", UVM_HIGH)

    def check_tx_level_threshold(self):
        threshold = self.regs.read_reg_value("fifo_control") & 0b1111
        uvm_info(self.tag, f"TX threshold = {threshold} size = {self.fifo_tx.qsize()}", UVM_HIGH)
        if self.fifo_tx.qsize() < threshold:
            if not self.fifo_tx_threshold:
                self.fifo_tx_threshold = True
                uvm_info(self.tag, "[interrupt flag] Enabling TX FIFO thread", UVM_HIGH)
        else:
            if self.fifo_tx_threshold:
                self.fifo_tx_threshold = False
                uvm_info(self.tag, "[interrupt flag] Disabling TX FIFO thread", UVM_HIGH)


uvm_component_utils(EF_UART)


class TX_QUEUE(Queue):
    """same queue provided by cocotb but with 2 new functions to get the tx value send it and then pop it from the queue after sending
    """
    def __init__(self, maxsize: int = 0):
        super().__init__(maxsize)

    async def get_no_pop(self):
        """same as get but without popping it from the queue
        """
        while self.empty():
            event = Event("{} get".format(type(self).__name__))
            self._getters.append((event, cocotb.scheduler._current_task))
            await event.wait()
        return self._queue[0]

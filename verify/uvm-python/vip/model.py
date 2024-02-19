import cocotb
from cocotb.triggers import Timer, Event, First
from cocotb.clock import Clock
from cocotb.binary import BinaryValue
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info, uvm_warning, uvm_error
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW, UVM_MEDIUM
from cocotb.queue import Queue
import asyncio
from uart_item.uart_item import uart_item
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
        self.flags = Flags(self.regs, self.tag)
        cocotb.scheduler.add(self.control_regs())

    def reset(self):
        self.write_register(0x8, 0)
        self.fifo_tx = TX_QUEUE(maxsize=16)
        self.fifo_tx_threshold = True
        self.fifo_rx = Queue(maxsize=16)
        self.fifo_rx_threshold = False
        self.flags = Flags(self.regs, self.tag)
        uvm_info(self.tag, f"Vip reset {self.fifo_tx.qsize()}", UVM_MEDIUM)

    def write_register(self, addr, data):
        uvm_info(self.tag, "Writing register " + hex(addr) + " with value " + hex(data), UVM_HIGH)
        self.regs.write_reg_value(addr, data)
        if addr == self.regs.reg_name_to_address["TXDATA"]:  # txdata
            try:
                word_mask = (1 << (self.regs.read_reg_value("CFG") & 0xf)) -1
                self.fifo_tx.put_nowait(data & word_mask)
                uvm_info(self.tag, f"value {hex(data)} written to tx fifo size = {self.fifo_tx.qsize()}", UVM_MEDIUM)
                self.check_tx_level_threshold()
                if self.fifo_tx.full():
                    self.flags.set_tx_full()
            except asyncio.QueueFull:
                uvm_warning(self.tag, f"writing to tx while fifo is full so ignore the value {hex(data)}")
        if addr == self.regs.reg_name_to_address["CTRL"]:  # control
            uvm_info(self.tag, "UART control reg set", UVM_HIGH)
            self.event_control.set()

    def read_register(self, addr):
        uvm_info(self.tag, "Reading register " + hex(addr), UVM_MEDIUM)
        if addr == self.regs.reg_name_to_address["RXDATA"]:  # reading from rx data
            try:
                uvm_info(self.tag, f"reading from rx fifo size = {self.fifo_rx.qsize()}", UVM_MEDIUM)
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
            tr = uart_item.type_id.create("tr", self)
            tr.char = data_tx
            tr.direction = uart_item.TX
            parity_type = (self.regs.read_reg_value("CFG") >> 5) & 0x7
            tr.calculate_parity(parity_type)
            tr.word_length = self.regs.read_reg_value("CFG") & 0xf
            
            await self.tx_trig_event.wait()
            self.ip_export.write(tr)
            self.tx_trig_event.clear()
            # pop last value from as it is sent
            # update rx fifo when loopback is enabled 
            await self.fifo_tx.get()

            if (self.regs.read_reg_value("CTRL") & 0xF) == 0xF:
                try:
                    self.fifo_rx.put_nowait(data_tx)
                    self.check_receiver_match(data_tx)
                    self.check_rx_level_threshold()
                    if self.fifo_rx.full():
                        self.flags.set_rx_full()
                except asyncio.QueueFull:
                    self.check_receiver_match(data_tx)
                    uvm_warning(self.tag, "writing to rx while fifo is full so ignore the value")
                    self.flags.set_overrun_err()

    def write_rx(self, tr):
        # if rx is enabled
        if (self.regs.read_reg_value("CTRL") & 7) in [5, 7]:
            try:
                self.fifo_rx.put_nowait(tr.char)
                self.check_receiver_match(tr.char)
                self.check_rx_level_threshold()
                self.new_rx_received.set()
                if self.fifo_rx.full():
                    self.flags.set_rx_full()
                    self.regs.write_reg_value("ris", 0b1, mask=0x1)
            except asyncio.QueueFull:
                self.new_rx_received.set()
                self.check_receiver_match(tr.char)
                uvm_warning(self.tag, "writing to rx while fifo is full so ignore the value")
                self.flags.set_overrun_err()
        else:
            uvm_warning(self.tag, "received uart transaction while uart is disabled")

    async def control_regs(self):
        while True:
            if (self.regs.read_reg_value("CTRL") & 7) in [3, 7]:
                uvm_info(self.tag, "Enabling UART TX", UVM_MEDIUM)
                if self.tx_thread is None:
                    self.tx_thread = await cocotb.start(self.transmit())
            elif self.tx_thread is not None:
                uvm_info(self.tag, "Disabling UART TX", UVM_MEDIUM)
                self.tx_thread.kill()
                self.tx_thread = None

            uvm_info(self.tag, "UART control reg wait", UVM_HIGH)
            await self.event_control.wait()
            uvm_info(self.tag, "UART control reg changed", UVM_HIGH)
            self.event_control.clear()

    def check_receiver_match(self, new_char):
        match_reg = self.regs.read_reg_value("MATCH")
        if new_char == match_reg:
            self.flags.set_data_match()

    def check_rx_level_threshold(self):
        threshold = (self.regs.read_reg_value("FIFOCTRL") >> 8) & 0b1111
        uvm_info(self.tag, f"RX threshold = {threshold} size = {self.fifo_rx.qsize()}", UVM_HIGH)
        if self.fifo_rx.qsize() > threshold:
            if not self.fifo_rx_threshold:
                self.fifo_rx_threshold = True
                self.flags.set_rx_above_threshold()
        # else:
        #     if self.fifo_rx_threshold:
        #         self.fifo_rx_threshold = False
        #         uvm_info(self.tag, "[interrupt flag] Disabling RX FIFO thread", UVM_HIGH)

    def check_tx_level_threshold(self):
        threshold = self.regs.read_reg_value("FIFOCTRL") & 0b1111
        uvm_info(self.tag, f"TX threshold = {threshold} size = {self.fifo_tx.qsize()}", UVM_HIGH)
        if self.fifo_tx.qsize() < threshold:
            if not self.fifo_tx_threshold:
                self.fifo_tx_threshold = True
                self.flags.set_tx_below_threshold()
        # else:
        #     if self.fifo_tx_threshold:
        #         self.fifo_tx_threshold = False
        #         uvm_info(self.tag, "[interrupt flag] Disabling TX FIFO thread", UVM_HIGH)


uvm_component_utils(EF_UART)


class Flags:
    def __init__(self, regs, tag="Flags"):
        self.regs = regs
        self.tag = tag
        self.mis_changed = Event()


    def write_interrupt(self, mask, name="None"):
        self.regs.write_reg_value("ris", mask, mask=mask)
        if self.regs.read_reg_value("im") & mask == mask and self.regs.read_reg_value("mis") & mask == 0:
            uvm_info(self.tag, f"Write interrupt {name}", UVM_MEDIUM)
            self.regs.write_reg_value("mis", mask, mask=mask, force_write=True)
            self.mis_changed.set()

    def clear_interrupt(self, mask, name="None"):
        self.regs.write_reg_value("mis", mask, mask=mask)
        if self.regs.read_reg_value("mis") & mask == mask:
            uvm_info(self.tag, f"Clear interrupt {name}", UVM_MEDIUM)
            self.regs.write_reg_value("mis", 0, mask=mask, force_write=True)
            self.mis_changed.set()

    def set_rx_full(self):
        uvm_info(self.tag, "[interrupt flag] RX FIFO is full", UVM_MEDIUM)
        self.write_interrupt(0b1, "RX FIFO full")


    def clr_rx_full(self):
        if self.regs.read_reg_value("ris") & 0b1:
            uvm_info(self.tag, "[clear flag] clear RX FIFO full interrupt", UVM_MEDIUM)
            self.clear_interrupt(mask=0b1, name="RX FIFO full")

    def set_tx_full(self):
        uvm_info(self.tag, "[interrupt flag] TX FIFO is full", UVM_MEDIUM)
        self.write_interrupt(0b10, "TX FIFO full")

    def clr_tx_full(self):
        if self.regs.read_reg_value("ris") & 0b10 == 0b10:
            uvm_info(self.tag, "[clear flag] clear TX FIFO full interrupt", UVM_MEDIUM)
            self.clear_interrupt(mask=0b10, name="TX FIFO full")

    def set_rx_above_threshold(self):
        uvm_info(self.tag, "[interrupt flag] RX FIFO above threshold", UVM_MEDIUM)
        self.write_interrupt(0b100, "RX FIFO above threshold")

    def clr_rx_above_threshold(self):
        if self.regs.read_reg_value("ris") & 0b100 == 0b100:
            uvm_info(self.tag, "[clear flag] clear RX FIFO above threshold interrupt", UVM_MEDIUM)
            self.clear_interrupt(mask=0b100, name="RX FIFO above threshold")

    def set_tx_below_threshold(self):
        uvm_info(self.tag, "[interrupt flag] TX FIFO below threshold", UVM_MEDIUM)
        self.write_interrupt(0b1000, "TX FIFO below threshold")

    def clr_tx_below_threshold(self):
        if self.regs.read_reg_value("ris") & 0b1000 == 0b1000:
            uvm_info(self.tag, "[clear flag] clear TX FIFO below threshold interrupt", UVM_MEDIUM)
            self.clear_interrupt(mask=0b1000, name="TX FIFO below threshold")

    def set_line_break(self):
        uvm_info(self.tag, "[interrupt flag] Line break", UVM_MEDIUM)
        self.write_interrupt(0b10000, "Line break")

    def clr_line_break(self):
        if self.regs.read_reg_value("ris") & 0b10000 == 0b10000:
            uvm_info(self.tag, "[clear flag] clear Line break interrupt", UVM_MEDIUM)
            self.clear_interrupt(mask=0b10000, name="Line break")

    def set_data_match(self):
        uvm_info(self.tag, "[interrupt flag] Data match", UVM_MEDIUM)
        self.write_interrupt(0b100000, "Data match")

    def clr_data_match(self):
        if self.regs.read_reg_value("ris") & 0b100000 == 0b100000:
            uvm_info(self.tag, "[clear flag] clear data match interrupt", UVM_MEDIUM)
            self.clear_interrupt(mask=0b100000, name="Data match")

    def set_frame_err(self):
        uvm_info(self.tag, "[interrupt flag] Frame error", UVM_MEDIUM)
        self.write_interrupt(0b1000000, "Frame error")

    def clr_frame_err(self):
        if self.regs.read_reg_value("ris") & 0b1000000 == 0b1000000:
            uvm_info(self.tag, "[clear flag] clear frame error interrupt", UVM_MEDIUM)
            self.clear_interrupt(mask=0b1000000, name="Frame error")

    def set_parity_err(self):
        uvm_info(self.tag, "[interrupt flag] Parity error", UVM_MEDIUM)
        self.write_interrupt(0b10000000, "Parity error")

    def clr_parity_err(self):
        if self.regs.read_reg_value("ris") & 0b10000000 == 0b10000000:
            uvm_info(self.tag, "[clear flag] clear Parity interrupt", UVM_MEDIUM)
            self.clear_interrupt(mask=0b10000000, name="Parity error")

    def set_overrun_err(self):
        uvm_info(self.tag, "[interrupt flag] Overrun error", UVM_MEDIUM)
        self.write_interrupt(0b100000000, "Overrun error")

    def clr_overrun_err(self):
        if self.regs.read_reg_value("ris") & 0b100000000 == 0b100000000:
            uvm_info(self.tag, "[clear flag] clear Overrun interrupt", UVM_MEDIUM)
            self.clear_interrupt(mask=0b100000000, name="Overrun error")

    def set_timeout_err(self):
        uvm_info(self.tag, "[interrupt flag] receiver Timeout error", UVM_MEDIUM)
        self.write_interrupt(0b1000000000, "receiver Timeout error")

    def clr_timeout_err(self):
        if self.regs.read_reg_value("ris") & 0b1000000000 == 0b1000000000:
            uvm_info(self.tag, "[clear flag] clear Timeout interrupt", UVM_MEDIUM)
            self.clear_interrupt(mask=0b1000000000, name="receiver Timeout error")


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

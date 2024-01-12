import cocotb
from cocotb.triggers import Timer, Event
from cocotb.clock import Clock
from cocotb.binary import BinaryValue
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info,uvm_warning
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW
from cocotb.queue import Queue
import asyncio


class EF_UART:
    def __init__(self, regs):
        # Initialize with parameters from the JSON
        self.regs_dict = regs.get_regs()
        self.regs = regs
        self.tag = "EF_UART_model"
        self.fifo_tx = Queue(maxsize=16)
        self.fifo_rx = Queue(maxsize=16)
        self.tx_thread = None
        self.rx_thread = None
        self.rx_data_is_x = True
        self.event_control = Event()
        cocotb.scheduler.add(self.control_regs())
        pass

    def write_register(self, addr, data):
        uvm_info(self.tag, "Writing register " + hex(addr) + " with value " + hex(data), UVM_MEDIUM)
        self.regs.write_reg_value(addr, data)
        if addr == 0x4:  # txdata
            try:
                self.fifo_tx.put_nowait(data)
            except asyncio.QueueFull:
                uvm_warning(self.tag, f"writing to tx while fifo is full so ignore the value {hex(data)}")
        if addr == 0x8:  # control
            uvm_info(self.tag, "UART control reg set", UVM_MEDIUM)
            self.event_control.set()

    def read_register(self, addr):
        uvm_info(self.tag, "Reading register " + hex(addr), UVM_MEDIUM)
        if addr == 0x4:  # txdata write only
            return 0xDEADBEEF
        elif addr == 0x0 and self.rx_data_is_x:  # rxdata
            return "00000000000000000000000xxxxxxxxx"
        elif addr == 0x20:  # txlevel
            uvm_info(self.tag, "TX level: " + str(self.fifo_tx.qsize()), UVM_MEDIUM)
            return self.fifo_tx.qsize()
        return self.regs.read_reg_value(addr)

    async def transmit(self):
        # this should be called only if uart is enabled
        while (True):
            data_tx = await self.fifo_tx.get()
            uvm_info(self.tag, "Transmitting " + hex(data_tx), UVM_MEDIUM)

    async def receive(self):
        while True:
            data_rx = await self.fifo_rx.get()
            self.rx_data_is_x = False
            self.regs.write_reg_value(0x0, data_rx)

    async def control_regs(self):
        while True:
            if (self.regs_dict[0x1C]["val"] & 7) in [3, 7]:
                uvm_info(self.tag, "Enabling UART TX", UVM_MEDIUM)
                if self.tx_thread is None:
                    self.tx_thread = await cocotb.start(self.transmit())
            elif self.tx_thread is not None:
                uvm_info(self.tag, "Disabling UART TX", UVM_MEDIUM)
                self.tx_thread.kill()
                self.tx_thread = None

            if self.regs_dict[0x1C]["val"] & 7 in [5, 7]:
                uvm_info(self.tag, "Enabling UART RX", UVM_MEDIUM)
                if self.rx_thread is None:
                    self.rx_thread = await cocotb.start(self.receive())
            elif self.rx_thread is not None:
                uvm_info(self.tag, "Disabling UART RX", UVM_MEDIUM)
                self.rx_thread.kill()
                self.rx_thread = None
            uvm_info(self.tag, "UART control reg wait", UVM_MEDIUM)
            await self.event_control.wait()
            uvm_info(self.tag, "UART control reg changed", UVM_MEDIUM)
            self.event_control.clear()

    async def tx_enable_watcher(self):
        while True:
            if self.regs_dict[0x1C]["val"] & 7 in [3, 7]:
                self.tx_thread = await cocotb.start_soon(self.transmit())
            else:
                if self.tx_thread is not None:
                    self.tx_thread.kill()
                    self.tx_thread = None
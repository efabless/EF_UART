from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_info, uvm_fatal
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from uvm.base import sv, UVM_HIGH, UVM_LOW
from uart_item.uart_item import uart_item
import random
from EF_UVM.bus_env.bus_seq_lib.bus_seq_base import bus_seq_base
from uart_seq_lib.uart_config import uart_config
from uart_seq_lib.tx_seq import tx_seq
from uart_seq_lib.rx_seq import rx_seq
from cocotb.triggers import NextTimeStep

class uart_prescalar_seq(UVMSequence):

    def __init__(self, handshake_event, name="uart_prescalar_seq"):
        UVMSequence.__init__(self, name)
        self.set_automatic_phase_objection(1)
        self.req = uart_item()
        self.rsp = uart_item()
        self.tag = name
        self.handshake_event = handshake_event

    async def body(self):
        # configure uart
        while True:
            await self.handshake_event.wait()
            self.handshake_event.clear()
            await uvm_do(self, rx_seq())
            self.handshake_event.set()


class uart_prescalar_seq_wrapper(bus_seq_base):

    def __init__(self, handshake_event, name="uart_prescalar_seq_wrapper"):
        super().__init__(name)
        self.handshake_event = handshake_event
        prescale_ranges = [(0x0, 0xf), (0x10, 0xff), (0x100, 0xfff), (0x1000, 0xffff)]
        prescale_ranges = [(0x0, 0xf), (0x10, 0xff), (0x100, 0xfff)] # remove the longest prescale so it would take less time
        self.prescaler_vals = [random.randint(range[0], range[1]) for range in prescale_ranges]
        random.shuffle(self.prescaler_vals)
        self.tx_seq_obj = tx_seq()

    async def body(self):
        # reset then set new prescalar
        for prescaler_val in self.prescaler_vals:
            uvm_info(self.get_type_name(), f"prescaler_val = {prescaler_val}", UVM_LOW)
            await self.send_reset()
            await uvm_do(self, uart_config(im=0, prescaler=prescaler_val))
            self.handshake_event.set()
            await uvm_do(self, self.tx_seq_obj)
            # await NextTimeStep() # wait dummy delay until event is clear
            await self.handshake_event.wait() # wait until the sequencer in the ip sequencer is done
            self.handshake_event.clear()

uvm_object_utils(uart_prescalar_seq)
uvm_object_utils(uart_prescalar_seq_wrapper)

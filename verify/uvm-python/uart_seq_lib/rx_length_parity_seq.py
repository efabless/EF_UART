from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_sequence_defines import uvm_do_with
from uvm.base import sv, UVM_HIGH, UVM_LOW
import random
from EF_UVM.bus_env.bus_seq_lib.bus_seq_base import bus_seq_base
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from uart_seq_lib.uart_config import uart_config
from uvm.seq import UVMSequence
from uart_item.uart_item import uart_item
from uart_seq_lib.rx_seq import rx_seq
from cocotb.triggers import NextTimeStep


class rx_length_parity_seq(UVMSequence):
    def __init__(self, handshake_event, name="rx_length_parity_seq"):
        UVMSequence.__init__(self, name)
        self.handshake_event = handshake_event
        self.req = uart_item()
        self.rsp = uart_item()
        lengths = [5, 6, 7, 8, 9]
        parity = [0, 1, 0b10, 0b100, 0b101]
        self.all_comb = [(l, p) for l in lengths for p in parity]
        random.shuffle(self.all_comb)

    async def body(self):
        while True:
            await self.handshake_event.wait()
            self.handshake_event.clear()
            await uvm_do(self, rx_seq(repeat=random.randint(30, 100)))
            self.handshake_event.set()
            await NextTimeStep()  # wait dummy delay until event is clear


class rx_length_parity_seq_wrapper(bus_seq_base):
    def __init__(self, handshake_event, name="rx_length_parity_seq_wrapper"):
        super().__init__(name)
        self.handshake_event = handshake_event
        lengths = [5, 6, 7, 8, 9]
        parity = [0, 1, 0b10, 0b100, 0b101]
        self.all_comb = [(l, p) for l in lengths for p in parity]
        random.shuffle(self.all_comb)

    async def body(self):
        for length, parity in self.all_comb:
            await self.send_reset()
            config = length | (parity << 5) | (random.randint(0, 1) << 4) | 0x3F << 8
            await uvm_do(self, uart_config(im=0, config=config))
            self.handshake_event.set()
            await NextTimeStep()  # wait dummy delay until event is clear
            await self.handshake_event.wait()  # wait until the sequencer in the ip sequencer is done
            self.handshake_event.clear()


uvm_object_utils(rx_length_parity_seq)
uvm_object_utils(rx_length_parity_seq_wrapper)

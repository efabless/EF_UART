from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_sequence_defines import uvm_do_with
from uvm.base import sv, UVM_HIGH, UVM_LOW
from EF_UVM.bus_env.bus_item import bus_bus_item
import random
from uart_seq_lib.seq_base import seq_base
from uvm.macros.uvm_message_defines import uvm_info, uvm_fatal
from EF_UVM.bus_env.bus_seq_lib.reset_seq import reset_seq
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from uart_seq_lib.uart_config import uart_config
from uart_seq_lib.tx_seq import tx_seq


class tx_length_parity_seq(seq_base):
    def __init__(self, name="tx_length_parity_seq"):
        super().__init__(name)
        lengths = [5, 6, 7, 8, 9]
        parity = [0, 1, 0b10, 0b100, 0b101]
        self.all_comb = [(l, p) for l in lengths for p in parity]
        random.shuffle(self.all_comb)
        self.tx_seq_obj = tx_seq(repeat=random.randint(7, 20))

    async def body(self):
        for length, parity in self.all_comb:
            await uvm_do(self, reset_seq())
            config = length | (parity << 5) | (random.randint(0, 1) << 4) | 0x3F << 8
            await uvm_do(self, uart_config(im=0, config=config))
            await uvm_do(self, self.tx_seq_obj)


uvm_object_utils(tx_length_parity_seq)

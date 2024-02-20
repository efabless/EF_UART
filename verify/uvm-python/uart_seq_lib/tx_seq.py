from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_sequence_defines import uvm_do_with
from uvm.base import sv, UVM_HIGH, UVM_LOW
from EF_UVM.wrapper_env.wrapper_item import wrapper_bus_item
import random
from uart_seq_lib.seq_base import seq_base


class tx_seq(seq_base):
    def __init__(self, name="tx_seq", repeat=1):
        super().__init__(name)
        self.repeat = repeat

    async def body(self):
        # configure uart
        for _ in range(self.repeat):
            random_send = random.randint(1, 16)
            for __ in range(random_send):
                await self.send_tx()
            for __ in range(random_send):
                await self.wait_tx()

    async def send_tx(self):
        await uvm_do_with(self, self.req, lambda addr: addr == 0x4, lambda kind: kind == wrapper_bus_item.WRITE, lambda data: data in range(0, 0x200))

    async def wait_tx(self):
        await self.monitor.tx_received.wait()
        self.monitor.tx_received.clear()


uvm_object_utils(tx_seq)
from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_info, uvm_fatal
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from uvm.base import sv, UVM_HIGH, UVM_LOW
from EF_UVM.bus_env.bus_item import bus_item
from EF_UVM.bus_env.bus_seq_lib.bus_seq_base import bus_seq_base


class uart_config(bus_seq_base):
    def __init__(
        self,
        name="uart_config",
        prescaler=None,
        config=None,
        im=None,
        match=None,
        fifo_control=None,
        control=None,
    ):
        super().__init__(name)
        self.prescaler = prescaler
        self.config = config
        self.im = im
        self.match = match
        self.fifo_control = fifo_control
        self.control = control

    async def body(self):
        await super().body()
        # get register names/address conversion dict

        # randomly config uart
        # first disabled the uart
        await self.send_req(
            is_write=True, reg="CTRL", data_condition=lambda data: data == 0
        )

        # random prescale value
        if self.prescaler is not None:
            await self.send_req(
                is_write=True,
                reg="PR",
                data_condition=lambda data: data == self.prescaler,
            )
        else:
            await self.send_req(
                is_write=True,
                reg="PR",
                data_condition=lambda data: data in range(0, 0x10),
            )

        # random config
        if self.config is not None:
            await self.send_req(
                is_write=True,
                reg="CFG",
                data_condition=lambda data: data == self.config,
            )
        else:
            await self.send_req(
                is_write=True,
                reg="CFG",
                data_condition=lambda data: (
                    (data >> 8) == 0x3F
                    and (data & 0xF) in range(5, 10)
                    and ((data & 0xE0) >> 5) in [0, 1, 2, 4, 5]
                    and data & 0xF == 9
                ),
            )

        # random IM
        if self.im is not None:
            await self.send_req(
                is_write=True, reg="im", data_condition=lambda data: data == self.im
            )
        else:
            await self.send_req(is_write=True, reg="im")

        # match register
        if self.match is not None:
            await self.send_req(
                is_write=True,
                reg="MATCH",
                data_condition=lambda data: data == self.match,
            )
        else:
            await self.send_req(is_write=True, reg="MATCH")

        # threshold value
        if self.fifo_control is not None:
            await self.send_req(
                is_write=True,
                reg="FIFOCTRL",
                data_condition=lambda data: data == self.fifo_control,
            )
        else:
            await self.send_req(
                is_write=True,
                reg="FIFOCTRL",
                data_condition=lambda data: ((data >> 8) & 0b1111) in range(0, 15)
                and (data & 0b1111) in range(0, 15),
            )

        # enable uart
        if self.control is not None:
            await self.send_req(
                is_write=True,
                reg="CTRL",
                data_condition=lambda data: data == self.control,
            )
        else:
            await self.send_req(
                is_write=True,
                reg="CTRL",
                data_condition=lambda data: data & 0b1111 == 0x7,
            )  # tx enabled, rx enabled and loopback disabled

    async def send_req(self, is_write, reg, data_condition=None):
        # send request
        self.create_new_item()
        if is_write:
            if data_condition is None:
                await uvm_do_with(
                    self,
                    self.req,
                    lambda addr: addr == self.adress_dict[reg],
                    lambda kind: kind == bus_item.WRITE,
                )
            else:
                await uvm_do_with(
                    self,
                    self.req,
                    lambda addr: addr == self.adress_dict[reg],
                    lambda kind: kind == bus_item.WRITE,
                    data_condition,
                )
        else:
            await uvm_do_with(
                self,
                self.req,
                lambda addr: addr == self.adress_dict[reg],
                lambda kind: kind == bus_item.READ,
            )


uvm_object_utils(uart_config)

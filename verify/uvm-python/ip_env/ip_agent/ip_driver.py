from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info, uvm_warning
from uvm.comps.uvm_driver import UVMDriver
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW, UVM_HIGH
from ip_env.ip_item import ip_item
from cocotb.triggers import Timer, ClockCycles, FallingEdge, Event, RisingEdge


class ip_driver(UVMDriver):
    def __init__(self, name="ip_driver", parent=None):
        super().__init__(name, parent)
        self.tag = name

    def build_phase(self, phase):
        super().build_phase(phase)
        arr = []
        if (not UVMConfigDb.get(self, "", "ip_if", arr)):
            uvm_fatal(self.tag, "No interface specified for self driver instance")
        else:
            self.sigs = arr[0]
        regs_arr = []
        if (not UVMConfigDb.get(self, "", "wrapper_regs", regs_arr)):
            uvm_fatal(self.tag, "No json file wrapper regs")
        else:
            self.regs = regs_arr[0]

    async def run_phase(self, phase):
        uvm_info(self.tag, "run_phase started", UVM_LOW)
        await self.reset()
        while True:
            tr = []
            await self.seq_item_port.get_next_item(tr)
            tr = tr[0]
            if tr.direction == ip_item.RX:
                uvm_info(self.tag, "Driving trans into IP: " + tr.convert2string(), UVM_MEDIUM)
                await self.start_of_rx()
                await self.send_byte(tr.char)
                await self.end_of_rx()
            else:
                uvm_warning(self.tag, f"invalid direction {tr.direction} send to driver", UVM_MEDIUM)
            self.seq_item_port.item_done()

    async def start_of_rx(self):
        self.sigs.RX.value = 0
        self.num_cyc_bit = self.get_bit_n_cyc()
        self.word_length = self.get_n_bits()
        await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)

    async def send_byte(self, byte):
        for i in range(self.word_length):
            self.sigs.RX.value = (byte >> i) & 1
            await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)

    async def end_of_rx(self):
        self.sigs.RX.value = 1
        await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)

    def get_bit_n_cyc(self):
        prescale = self.regs.read_reg_value("prescaler")
        uvm_info(self.tag, "prescale = " + str(prescale), UVM_HIGH)
        return ((prescale + 1) * 8)

    def get_n_bits(self):
        word_length = self.regs.read_reg_value("config") & 0xf
        uvm_info(self.tag, "Data word length = " + str(word_length), UVM_MEDIUM)
        return word_length

    async def reset(self, num_cycles=3):
        self.sigs.RX.value = 1
        await ClockCycles(self.sigs.PCLK, num_cycles)



uvm_component_utils(ip_driver)

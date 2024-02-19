from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info, uvm_warning
from uvm.comps.uvm_driver import UVMDriver
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW, UVM_MEDIUM
from uart_item.uart_item import uart_item
from cocotb.triggers import Timer, ClockCycles, FallingEdge, Event, RisingEdge
import cocotb
import random


class uart_driver(UVMDriver):
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
            self.sigs = arr[0]
        glitches_arr = []
        if (not UVMConfigDb.get(self, "", "insert_glitches", glitches_arr)):
            self.insert_glitches = False
        else:
            self.insert_glitches = glitches_arr[0]

    async def run_phase(self, phase):
        uvm_info(self.tag, "run_phase started", UVM_LOW)
        await self.reset()
        # assert glitches 
        while True:
            tr = []
            await self.seq_item_port.get_next_item(tr)
            tr = tr[0]
            if tr.direction == uart_item.RX:
                uvm_info(self.tag, "Driving trans into IP: " + tr.convert2string(), UVM_MEDIUM)
                await self.start_of_rx()
                if self.insert_glitches:
                    await cocotb.start(self.add_glitches()) # assert glitches
                await self.send_byte(tr.char)
                uvm_info(self.tag, "finish send byte", UVM_MEDIUM)
                await self.send_parity(tr)
                uvm_info(self.tag, "finish send parity", UVM_MEDIUM)
                await self.send_stop_bit()
                uvm_info(self.tag, "finish send bit1", UVM_MEDIUM)
                await self.end_of_rx(1)
                uvm_info(self.tag, "finish send bit0", UVM_MEDIUM)
                # add breakline 2% of the times 
                # if random.random() < 0.02:
                #     uvm_info(self.tag, "Adding breakline", UVM_MEDIUM)
                #     await self.break_line()   
            else:
                uvm_warning(self.tag, f"invalid direction {tr.direction} send to driver", UVM_HIGH)
            self.seq_item_port.item_done()

    async def break_line(self):
        self.sigs.RX.value = 0
        await ClockCycles(self.sigs.PCLK, self.num_cyc_bit * random.randint(12, 20))
        self.sigs.RX.value = 1
        await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)

    async def start_of_rx(self):
        self.sigs.RX.value = 0
        self.num_cyc_bit = self.get_bit_n_cyc()
        self.word_length = self.get_n_bits()
        uvm_info(self.tag, "starting of start bit", UVM_HIGH)
        await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)
        uvm_info(self.tag, "finifhing of start bit", UVM_HIGH)

    async def send_byte(self, byte):
        for i in range(self.word_length):
            self.sigs.RX.value = (byte >> i) & 1
            uvm_info(self.tag, f"driving byte[{i}] = {(byte >> i) & 1}", UVM_HIGH)
            await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)

    async def send_parity(self, tr):
        parity_type = (self.regs.read_reg_value("CFG") >> 5) & 0x7
        tr.calculate_parity(parity_type)
        if tr.parity == "None":
            return
        self.sigs.RX.value = int(tr.parity)
        uvm_info(self.tag, f"driving parity = {tr.parity}", UVM_HIGH)
        await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)

    async def send_stop_bit(self):
        stop_bit = (self.regs.read_reg_value("CFG") >> 4) & 0x1
        if stop_bit:
            self.sigs.RX.value = 1
            uvm_info(self.tag, f"driving extra stop bit", UVM_HIGH)
            await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)
        return

    async def end_of_rx(self, extra_stop_bit=0):
        self.sigs.RX.value = 1
        uvm_info(self.tag, f"start ending of RX", UVM_HIGH)
        await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)
        uvm_info(self.tag, f"finished ending of RX", UVM_HIGH)
        for _ in range(extra_stop_bit):
            await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)

    def get_bit_n_cyc(self):
        prescale = self.regs.read_reg_value("PR")
        uvm_info(self.tag, "prescale = " + str(prescale), UVM_HIGH)
        return ((prescale + 1) * 8)

    def get_n_bits(self):
        word_length = self.regs.read_reg_value("CFG") & 0xf
        uvm_info(self.tag, "Data word length = " + str(word_length), UVM_HIGH)
        return word_length

    async def reset(self, num_cycles=3):
        self.sigs.RX.value = 1
        await ClockCycles(self.sigs.PCLK, num_cycles)

    async def add_glitches(self):
        await ClockCycles(self.sigs.PCLK, random.randint(self.num_cyc_bit, self.num_cyc_bit * 7))
        await Timer(random.randint(1, 100), units="ns")
        old_val = self.sigs.RX.value.integer
        self.sigs.RX.value = old_val-1
        uvm_info(self.tag, "Asserting glitch", UVM_MEDIUM)
        await Timer(random.randint(1, 10), units="ns")
        self.sigs.RX.value = old_val
        # wait long before checking again

uvm_component_utils(uart_driver)

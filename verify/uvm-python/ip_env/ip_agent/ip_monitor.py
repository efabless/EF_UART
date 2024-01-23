from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info, uvm_error
from uvm.comps.uvm_monitor import UVMMonitor
from uvm.tlm1.uvm_analysis_port import UVMAnalysisPort
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb.triggers import Timer, ClockCycles, FallingEdge, Event, RisingEdge, Combine
from ip_env.ip_item import ip_item
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW, UVM_HIGH
import math
import cocotb


class ip_monitor(UVMMonitor):
    def __init__(self, name="ip_monitor", parent=None):
        super().__init__(name, parent)
        self.monitor_port = UVMAnalysisPort("monitor_port", self)
        self.tag = name
        self.tx_received = Event("tx_received")
        self.rx_received = Event("rx_received")

    def build_phase(self, phase):
        super().build_phase(phase)
        arr = []
        if (not UVMConfigDb.get(self, "", "ip_if", arr)):
            uvm_fatal(self.tag, "No interface specified for self monitor instance")
        else:
            self.sigs = arr[0]
        regs_arr = []
        if (not UVMConfigDb.get(self, "", "wrapper_regs", regs_arr)):
            uvm_fatal(self.tag, "No json file wrapper regs")
        else:
            self.regs = regs_arr[0]

    async def run_phase(self, phase):
        sample_tx = await cocotb.start(self.sample_tx())
        sample_rx = await cocotb.start(self.sample_rx())
        await self.get_clk_period()
        await Combine(sample_tx, sample_rx)

    async def get_clk_period(self):
        time0 = cocotb.utils.get_sim_time(units="ns")
        await ClockCycles(self.sigs.PCLK, 1)
        time1 = cocotb.utils.get_sim_time(units="ns")
        self.clk_period = time1 - time0
        return

    async def sample_tx(self):
        while True:
            tr = ip_item.type_id.create("tr", self)
            # wait for a char
            tr.char, tr.parity, tr.word_length = await self.get_char()
            tr.direction = ip_item.TX
            uvm_info(self.tag, "sampled uart TX transaction: " + tr.convert2string(), UVM_MEDIUM)
            self.monitor_port.write(tr)
            self.tx_received.set()

    async def sample_rx(self):
        while True:
            tr = ip_item.type_id.create("tr", self)
            # wait for a char
            timeout_thread = await cocotb.start(self.watch_timeout())
            tr.char, tr.parity, tr.word_length = await self.get_char(ip_item.RX)
            tr.direction = ip_item.RX
            uvm_info(self.tag, "sampled uart RX transaction: " + tr.convert2string(), UVM_MEDIUM)
            self.monitor_port.write(tr)
            self.rx_received.set()
            timeout_thread.kill()

    async def get_char(self, direction=ip_item.TX):
        if (direction == ip_item.TX):
            num_cyc_bit, word_length = await self.start_of_tx()
            signal = self.sigs.TX
            done_signal = self.sigs.tx_done
        else:
            num_cyc_bit, word_length = await self.start_of_rx()
            signal = self.sigs.RX
            done_signal = self.sigs.rx_done
        char = ""
        parity = "None"
        for i in range(word_length):
            new_bit = await self.glitch_free_sample(signal, num_cyc_bit, 8)
            char = new_bit + char
            uvm_info(self.tag, f"char[{i}] = {new_bit}  length = {word_length}", UVM_MEDIUM)
        # get parity bit
        if self.is_parity_exists():
            parity = await self.glitch_free_sample(signal, num_cyc_bit, 8)
            uvm_info(self.tag, f"parity bit = {parity}  length = {word_length}", UVM_MEDIUM)
        await ClockCycles(self.sigs.PCLK, num_cyc_bit - 2)  # to even the /2 in the start of tx
        # mimic stop bit
        if self.is_stop_bit_exists():
            await ClockCycles(self.sigs.PCLK, num_cyc_bit)
        if direction == ip_item.TX:
            uvm_info(self.tag, f"waiting for {'tx' if direction == ip_item.TX else 'rx'}_done", UVM_MEDIUM)
            # wait for done from the model
            # check the monitor waited for the done less than num_cyc_bit_tx / 2 if not there is an issue in the protocol
            wait_done_time = cocotb.utils.get_sim_time(units="ns")
            while True:
                await RisingEdge(done_signal)  # for the fifo of the model to get the same timing as the fifo in rtl
                await Timer(1, "ns")
                if done_signal.value == 1: # to make sure it's no latch
                    await FallingEdge(done_signal)  # for the fifo of the model to get the same timing as the fifo in rtl
                    uvm_info(self.tag, f"found {'tx' if direction == ip_item.TX else 'rx'}_done", UVM_MEDIUM)
                    await Timer(1, "ns")
                    break
            done_time = cocotb.utils.get_sim_time(units="ns")
            uvm_info(self.tag, f"waited for done {(done_time - wait_done_time)/ self.clk_period} cycles num_cyc {num_cyc_bit}", UVM_MEDIUM)
            # check the monitor waited for the done less than num_cyc_bit_tx / 2 if not there is an issue in the protocol
            if (done_time - wait_done_time) / self.clk_period > num_cyc_bit / 2:
                uvm_error(self.tag, f"stop bit checker waited for the done more than {num_cyc_bit / 2} < {(done_time - wait_done_time)/ self.clk_period} cycles")
        return int(char, 2), parity, word_length

    async def start_of_tx(self):
        while True:
            await FallingEdge(self.sigs.TX)
            uvm_info(self.tag, "start of TX", UVM_MEDIUM)
            num_cyc_bit_tx = self.get_bit_n_cyc()
            word_length_tx = self.get_n_bits()
            await Timer(1, units="ns")
            if self.sigs.TX.value == 1:
                continue
            await ClockCycles(self.sigs.PCLK, num_cyc_bit_tx)
            break
        return num_cyc_bit_tx, word_length_tx

    async def start_of_rx(self):
        while True:
            await FallingEdge(self.sigs.RX)
            uvm_info(self.tag, "start of RX", UVM_MEDIUM)
            num_cyc_bit_rx = self.get_bit_n_cyc()
            word_length_rx = self.get_n_bits()
            await Timer(1, units="ns")
            if self.sigs.RX.value == 1:
                continue
            await ClockCycles(self.sigs.PCLK, num_cyc_bit_rx)
            break
        return num_cyc_bit_rx, word_length_rx

    def get_bit_n_cyc(self):
        prescale = self.regs.read_reg_value("prescaler")
        uvm_info(self.tag, "prescale = " + str(prescale), UVM_MEDIUM)
        return ((prescale + 1) * 8)

    def get_n_bits(self):
        word_length = self.regs.read_reg_value("config") & 0b1111
        uvm_info(self.tag, "Data word length = " + str(word_length), UVM_MEDIUM)
        return word_length

    def is_parity_exists(self):
        parity = (self.regs.read_reg_value("config") >> 5) & 0b111
        return parity != 0

    def is_stop_bit_exists(self):
        stop_bit = (self.regs.read_reg_value("config") >> 4) & 0x1
        return stop_bit

    async def watch_timeout(self):
        while True:
            timeout = (self.regs.read_reg_value("config") >> 8) & 0b111111
            counter = 0
            for _ in range(timeout):
                await ClockCycles(self.sigs.PCLK, self.get_bit_n_cyc())
                counter += 1
                uvm_info(self.tag, "timeout counter = " + str(counter) , UVM_MEDIUM)
            # if it reaches here it means it timed out
            uvm_info(self.tag, f"timed out for {timeout}", UVM_MEDIUM)

    async def glitch_free_sample(self, signal, num_cyc, sample_num):
        base_value = num_cyc // sample_num
        lst = [base_value] * sample_num
        # Distribute the remainder across the first 'remainder' elements of the list by adding 1
        remainder = num_cyc % sample_num
        ones = 0
        zeros = 0
        for i in range(remainder):
            lst[i] += 1
        # Count the number of ones and zeros
        for cyc in lst:
            val = signal.value.binstr
            if val == "1":
                ones += 1
            elif val == "0":
                zeros += 1
            await ClockCycles(self.sigs.PCLK, cyc)
        uvm_info(self.tag, f"finish glitch_free_sample ones = {ones} zeros = {zeros} sample rate = {sample_num} num_cyc = {num_cyc} list = {lst}", UVM_HIGH)
        if ones > zeros:
            return "1"
        elif ones < zeros:
            return "0"
        else:
            return "X"


uvm_component_utils(ip_monitor)

from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info, uvm_error, uvm_warning
from uvm.comps.uvm_monitor import UVMMonitor
from uvm.tlm1.uvm_analysis_port import UVMAnalysisPort
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb.triggers import Timer, ClockCycles, FallingEdge, Event, RisingEdge, Combine, First
from uart_item.uart_item import uart_item
from uart_item.uart_interrupt import uart_interrupt
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW, UVM_MEDIUM
import cocotb
import math
from EF_UVM.ip_env.ip_agent.ip_monitor import ip_monitor


class uart_monitor(ip_monitor):
    def __init__(self, name="uart_monitor", parent=None):
        super().__init__(name, parent)
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
        timeout_thread = await cocotb.start(self.watch_rx_timeout())
        break_line_thread = await cocotb.start(self.watch_line_break())
        await self.get_clk_period()
        await Combine(sample_tx, sample_rx)

    async def get_clk_period(self):
        await RisingEdge(self.sigs.PCLK)
        await RisingEdge(self.sigs.PCLK)
        time0 = cocotb.utils.get_sim_time(units="ns")
        await RisingEdge(self.sigs.PCLK)
        # await ClockCycles(self.sigs.PCLK, 1)
        time1 = cocotb.utils.get_sim_time(units="ns")
        self.clk_period = time1 - time0
        uvm_info(self.tag, f"clock period = {self.clk_period}", UVM_MEDIUM)
        return

    async def sample_tx(self):
        while True:
            tr = uart_item.type_id.create("tr", self)
            # wait for a char
            tr.char, tr.parity, tr.word_length = await self.get_char()
            tr.direction = uart_item.TX
            uvm_info(self.tag, "sampled uart TX transaction: " + tr.convert2string(), UVM_HIGH)
            self.monitor_port.write(tr)
            self.tx_received.set()

    async def sample_rx(self):
        while True:
            tr = uart_item.type_id.create("tr", self)
            # wait for a char
            tr.char, tr.parity, tr.word_length = await self.get_char(uart_item.RX)
            if tr.char == tr.parity == tr.word_length == "None":
                uvm_warning(self.tag, "ignore char sampled as the stop bit isn't detected")
                continue
            tr.direction = uart_item.RX
            uvm_info(self.tag, "sampled uart RX transaction: " + tr.convert2string(), UVM_MEDIUM)
            self.monitor_port.write(tr)
            self.rx_received.set()
            self.check_parity(tr.char, tr.parity)

    async def get_char(self, direction=uart_item.TX):
        if (direction == uart_item.TX):
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
            uvm_info(self.tag, f"char[{i}] = {new_bit}  length = {word_length}", UVM_HIGH)
        # get parity bit
        if self.is_parity_exists():
            parity = await self.glitch_free_sample(signal, num_cyc_bit, 8)
            uvm_info(self.tag, f"parity bit = {parity}  length = {word_length}", UVM_HIGH)
        # stop bit
        stop_bit = await self.glitch_free_sample(signal, num_cyc_bit, 8, last_bit=not self.is_stop_bit_exists())
        if stop_bit != "1":
            uvm_warning(self.tag, f"stop bit expected but got {stop_bit}")
            if direction == uart_item.RX:
                self.frame_error()
                return "None", "None", "None"
        # await ClockCycles(self.sigs.PCLK, num_cyc_bit - 2)  # to even the /2 in the start of tx
        # mimic stop bit
        if self.is_stop_bit_exists():
            stop_bit = await self.glitch_free_sample(signal, num_cyc_bit, 8, last_bit=True)
            if stop_bit != "1":
                uvm_warning(self.tag, f"stop bit expected but got {stop_bit}")
                if direction == uart_item.RX:
                    self.frame_error()
                    return "None", "None", "None"
        if direction == uart_item.TX:
            uvm_info(self.tag, f"waiting for {'tx' if direction == uart_item.TX else 'rx'}_done", UVM_MEDIUM)
            # wait for done from the model
            # check the monitor waited for the done less than num_cyc_bit_tx / 2 if not there is an issue in the protocol
            wait_done_time = cocotb.utils.get_sim_time(units="ns")
            while True:
                await RisingEdge(done_signal)  # for the fifo of the model to get the same timing as the fifo in rtl
                await Timer(1, "ns")
                if done_signal.value == 1: # to make sure it's no latch
                    await FallingEdge(done_signal)  # for the fifo of the model to get the same timing as the fifo in rtl
                    uvm_info(self.tag, f"found {'tx' if direction == uart_item.TX else 'rx'}_done", UVM_HIGH)
                    await Timer(1, "ns")
                    break
            done_time = cocotb.utils.get_sim_time(units="ns")
            uvm_info(self.tag, f"waited for done {(done_time - wait_done_time)/ self.clk_period} cycles num_cyc {num_cyc_bit}", UVM_HIGH)
            # check the monitor waited for the done less than num_cyc_bit_tx / 2 if not there is an issue in the protocol
            if (done_time - wait_done_time) / self.clk_period > num_cyc_bit / 2:
                uvm_error(self.tag, f"stop bit checker waited for the done more than {num_cyc_bit / 2} < {(done_time - wait_done_time)/ self.clk_period} cycles")
        return int(char, 2), parity, word_length

    async def start_of_tx(self):
        while True:
            await FallingEdge(self.sigs.TX)
            uvm_info(self.tag, "start of TX", UVM_HIGH)
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
            uvm_info(self.tag, "start of RX", UVM_HIGH)
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
        uvm_info(self.tag, "prescale = " + str(prescale), UVM_HIGH)
        return ((prescale + 1) * 8)

    def get_n_bits(self):
        word_length = self.regs.read_reg_value("config") & 0b1111
        uvm_info(self.tag, "Data word length = " + str(word_length), UVM_HIGH)
        return word_length

    def is_parity_exists(self):
        parity = (self.regs.read_reg_value("config") >> 5) & 0b111
        return parity != 0

    def is_stop_bit_exists(self):
        stop_bit = (self.regs.read_reg_value("config") >> 4) & 0x1
        return stop_bit

    async def watch_rx_timeout(self):
        # wait for uart enable
        while True:
            uart_enabled = self.regs.read_reg_value("control") & 1
            if uart_enabled:
                break
            await ClockCycles(self.sigs.PCLK, 1)
        while True:
            timeout = 1 + ((self.regs.read_reg_value("config") >> 8) & 0b111111)
            bit_rate = self.get_bit_n_cyc() * self.clk_period
            total_time_ns = int(timeout * bit_rate)
            uvm_info(self.tag, f"timeout = {timeout} bit_rate = {bit_rate} mult = {bit_rate * timeout}", UVM_MEDIUM)
            time_out = Timer(total_time_ns, "ns")   #time out condition
            new_rx = self.rx_received.wait()   #recieved new rx
            await First(time_out, new_rx)
            if self.rx_received.is_set():
                self.rx_received.clear()
            else:
                # if it reaches here it means it timed out
                irq = uart_interrupt.type_id.create("tr_irq", self)
                irq.rx_timeout = 1
                # uvm_info(self.tag, f"timed out for {timeout}", UVM_HIGH)
                self.monitor_irq_port.write(irq)

    async def watch_line_break(self):
        while True:
            await FallingEdge(self.sigs.RX)
            bit_num_cycles = self.get_bit_n_cyc()
            await ClockCycles(self.sigs.PCLK, math.floor(bit_num_cycles/2))
            for _ in range(11):
                await ClockCycles(self.sigs.PCLK, bit_num_cycles)
                if self.sigs.RX.value == 1:
                    break
            if self.sigs.RX.value == 1:
                continue
            irq = uart_interrupt.type_id.create("tr_irq", self)
            irq.rx_break_line = 1
            uvm_info(self.tag, "break line", UVM_HIGH)
            self.monitor_irq_port.write(irq)

    def check_parity(self, char, parity):
        tr = uart_item.type_id.create("tr", self)
        tr.char = char
        parity_type = (self.regs.read_reg_value("config") >> 5) & 0x7
        tr.calculate_parity(parity_type)
        if tr.parity == parity:
            return
        else:
            irq = uart_interrupt.type_id.create("tr_irq", self)
            irq.rx_wrong_parity = 1
            uvm_info(self.tag, f"wrong parity for char = {bin(char)} parity_type = {parity_type} parity = {parity} expected = {tr.parity}", UVM_MEDIUM)
            self.monitor_irq_port.write(irq)

    def frame_error(self):
        irq = uart_interrupt.type_id.create("tr_irq", self)
        irq.rx_frame_error = 1
        self.monitor_irq_port.write(irq)

    async def glitch_free_sample(self, signal, num_cyc, sample_num, last_bit=False):
        base_value = num_cyc // sample_num
        lst = [base_value] * sample_num
        # Distribute the remainder across the first 'remainder' elements of the list by adding 1
        remainder = num_cyc % sample_num
        ones = 0
        zeros = 0
        for i in range(remainder):
            lst[i] += 1
        if last_bit:
            lst.pop() # in the last bit leave time to wait for tx_done for tx only to sync the fifos
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


uvm_component_utils(uart_monitor)

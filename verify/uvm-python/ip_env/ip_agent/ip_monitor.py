from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.comps.uvm_monitor import UVMMonitor
from uvm.tlm1.uvm_analysis_port import UVMAnalysisPort
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb.triggers import Timer, ClockCycles, FallingEdge, Event, RisingEdge, Combine
from ip_env.ip_item import ip_item
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW
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
        await Combine(sample_tx, sample_rx)

    async def sample_tx(self):
        self.tx_received_counter = 0
        while True:
            tr = ip_item.type_id.create("tr", self)
            # wait for a char
            tr.char = await self.get_char()
            self.tx_received_counter += 1
            tr.direction = ip_item.TX
            uvm_info(self.tag, "sampled uart TX transaction: " + tr.convert2string(), UVM_MEDIUM)
            self.monitor_port.write(tr)
            self.tx_received.set()

    async def sample_rx(self):
        self.rx_received_counter = 0
        while True:
            tr = ip_item.type_id.create("tr", self)
            # wait for a char
            tr.char = await self.get_char_rx()
            self.rx_received_counter += 1
            tr.direction = ip_item.RX
            uvm_info(self.tag, "sampled uart RX transaction: " + tr.convert2string(), UVM_MEDIUM)
            self.monitor_port.write(tr)
            self.rx_received.set()

    async def get_char(self, direction=ip_item.TX):
        await self.start_of_tx()
        char = ""
        for i in range(8):
            char = self.sigs.TX.value.binstr + char
            await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)
        await ClockCycles(self.sigs.PCLK, math.floor(self.num_cyc_bit / 2))  # to even the /2 in the start of tx
        if self.tx_received_counter > 3: # first transmit might have diffrent delay because of the gen tick module
            await RisingEdge(self.sigs.tx_done)  # for the fifo of the model to get the same timing as the fifo in rtl
        return int(char, 2)

    async def start_of_tx(self):
        while True:
            await FallingEdge(self.sigs.TX)
            self.num_cyc_bit = self.get_bit_n_cyc()
            await Timer(1, units="ns")
            if self.sigs.TX.value == 1:
                continue
            await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)
            await ClockCycles(self.sigs.PCLK, math.ceil(self.num_cyc_bit / 2))
            break

    async def get_char_rx(self):
        await self.start_of_rx()
        char = ""
        for i in range(8):
            char = self.sigs.RX.value.binstr + char
            uvm_info(self.tag, f"char[{i}] = {self.sigs.RX.value.binstr} ", UVM_MEDIUM)
            await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)
        await ClockCycles(self.sigs.PCLK, math.floor(self.num_cyc_bit / 2))  # to even the /2 in the start of tx
        # uvm_info(self.tag, f"wait for rx done", UVM_MEDIUM)
        # if self.rx_received_counter > 3: # first transmit might have diffrent delay because of the gen tick module
        #     await RisingEdge(self.sigs.rx_done)  # for the fifo of the model to get the same timing as the fifo in rtl
        return int(char, 2)
    
    async def start_of_rx(self):
        while True:
            await FallingEdge(self.sigs.RX)
            uvm_info(self.tag, "start of RX", UVM_MEDIUM)
            self.num_cyc_bit = self.get_bit_n_cyc()
            await Timer(1, units="ns")
            if self.sigs.RX.value == 1:
                continue
            await ClockCycles(self.sigs.PCLK, self.num_cyc_bit)
            await ClockCycles(self.sigs.PCLK, math.ceil(self.num_cyc_bit / 2))
            break

    def get_bit_n_cyc(self):
        prescale = self.regs.read_reg_value("prescaler")
        uvm_info(self.tag, "prescale = " + str(prescale), UVM_MEDIUM)
        return ((prescale + 1) * 8)


uvm_component_utils(ip_monitor)

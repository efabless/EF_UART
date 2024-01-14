from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.comps.uvm_monitor import UVMMonitor
from uvm.tlm1.uvm_analysis_port import UVMAnalysisPort
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb.triggers import Timer, ClockCycles, FallingEdge, Event
from ip_env.ip_item import ip_item
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW
import math


class ip_monitor(UVMMonitor):
    def __init__(self, name="ip_monitor", parent=None):
        super().__init__(name, parent)
        self.monitor_port = UVMAnalysisPort("monitor_port", self)
        self.tag = name
        self.tx_received = Event("tx_received")


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
        while True:
            tr = ip_item.type_id.create("tr", self)
            # wait for a char
            tr.char = await self.get_char()
            tr.direction = ip_item.TX
            uvm_info(self.tag, "sampled uart transaction: " + tr.convert2string(), UVM_MEDIUM)
            self.monitor_port.write(tr)
            self.tx_received.set()

    async def get_char(self):
        await self.start_of_tx()
        char = ""
        for i in range(8):
            char = self.sigs.TX.value.binstr + char
            await ClockCycles(self.sigs.PCLK, self.get_rate_n_cyc())
        await ClockCycles(self.sigs.PCLK, math.ceil(self.get_rate_n_cyc() / 2))  # to even the /2 in the start of tx
        return chr(int(char, 2))

    async def start_of_tx(self):
        while True:
            await FallingEdge(self.sigs.TX)
            await Timer(1, units="ns")
            if self.sigs.TX.value == 1:
                continue
            await ClockCycles(self.sigs.PCLK, self.get_rate_n_cyc())
            await ClockCycles(self.sigs.PCLK, math.floor(self.get_rate_n_cyc() / 2))
            break

    def get_rate_n_cyc(self):
        prescale = self.regs.get_regs()[12]["val"]
        return (prescale + 1) * 8


uvm_component_utils(ip_monitor)

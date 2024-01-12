from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.comps.uvm_driver import UVMDriver
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb.triggers import Timer, RisingEdge
from uvm.base.uvm_object_globals import UVM_MEDIUM, UVM_LOW
from wrapper_env.wrapper_item import wrapper_bus_item


class wrapper_driver(UVMDriver):
    def __init__(self, name="wrapper_driver", parent=None):
        super().__init__(name, parent)
        self.tag = name

    def build_phase(self, phase):
        super().build_phase(phase)
        arr = []
        if (not UVMConfigDb.get(self, "", "wrapper_bus_if", arr)):
            uvm_fatal(self.tag, "No interface specified for self driver instance")
        else:
            self.sigs = arr[0]

    async def run_phase(self, phase):
        uvm_info(self.tag, "run_phase started", UVM_LOW)
        await self.reset()

        while True:
            await self.drive_delay()
            tr = []
            await self.seq_item_port.get_next_item(tr)
            tr = tr[0]
            uvm_info(self.tag, "Driving trans into DUT: " + tr.convert2string(), UVM_LOW)

            #if (not self.sigs.clk.triggered):
            #yield Edge(self.sigs.clk)
            await self.drive_delay()
            #yield RisingEdge(self.sigs.clk)
            #yield Timer(1, "NS")

            await self.trans_received(tr)
            #uvm_do_callbacks(apb_master,apb_master_cbs,trans_received(self,tr))

            if tr.kind == wrapper_bus_item.READ:
                data = []
                await self.read(tr.addr, data)
                tr.data = data[0]
            elif tr.kind == wrapper_bus_item.WRITE:
                await self.write(tr.addr, tr.data)

            await self.trans_executed(tr)
            #uvm_do_callbacks(apb_master,apb_master_cbs,trans_executed(self,tr))
            self.seq_item_port.item_done()

    async def reset(self, num_cycles=3):
        self.sigs.PRESETn.value = 0
        for _ in range(num_cycles):
            await self.drive_delay()
        self.sigs.PRESETn.value = 1

    async def drive_delay(self):
        await RisingEdge(self.sigs.PCLK)
        await Timer(1, "NS")

    async def trans_received(self, tr):
        await Timer(1, "NS")

    async def trans_executed(self, tr):
        await Timer(1, "NS")

    async def read(self, addr, data):
        uvm_info(self.tag, "Doing APB read to addr " + hex(addr), UVM_MEDIUM)

        self.sigs.PADDR.value = addr
        self.sigs.PWRITE.value = 0
        self.sigs.PSEL.value = 1
        await self.drive_delay()
        self.sigs.PENABLE.value = 1
        await self.drive_delay()
        data.append(self.sigs.PRDATA)
        self.sigs.PSEL.value = 0
        self.sigs.PENABLE.value = 0

    async def write(self, addr, data):
        uvm_info(self.tag, "Doing APB write to addr " + hex(addr), UVM_MEDIUM)
        self.sigs.PADDR.value = addr
        self.sigs.PWDATA.value = data
        self.sigs.PWRITE.value = 1
        self.sigs.PSEL.value = 1
        await self.drive_delay()
        self.sigs.PENABLE.value = 1
        await self.drive_delay()
        self.sigs.PSEL.value = 0
        self.sigs.PENABLE.value = 0
        uvm_info(self.tag, "Finished APB write to addr " + hex(addr), UVM_MEDIUM)


uvm_component_utils(wrapper_driver)

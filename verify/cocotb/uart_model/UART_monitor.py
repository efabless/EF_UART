import cocotb
from cocotb.triggers import Timer, RisingEdge, ClockCycles, FallingEdge, NextTimeStep, Edge
from collections import namedtuple


UART_Transaction = namedtuple("UART_Transaction", ["type", "char"])
APB_Transaction = namedtuple("APB_Transaction", ["address", "write", "data", "size"])


class UART_apbMonitor:
    def __init__(self, hdl, queue):
        self.uart_hdl = hdl
        self._queue_fork = cocotb.scheduler.add(self._apb_monitor_(queue))
        cocotb.log.debug("[TEST] Start UART APB Monitor")

    async def _apb_monitor_(self, queue):
        self.hdls()
        while True:
            await RisingEdge(self.en_hdl)
            if self.uart_irq_hdl.value.integer == 1:
                transaction = UART_Transaction(type="irq")
                queue.put_nowait(transaction)
                cocotb.log.debug(f"[{__class__.__name__}][_apb_monitor_] sending transaction {transaction} to queue")
                self.uart_irq_hdl.value = 0

    async def _monitor_(self, queue):
        self.hdls()
        bit_cycles = 26302
        cocotb.log.info(f"[{__class__.__name__}][_soc_debug_monitor] bit_cycles: {bit_cycles}")
        # while True:
        rx_fork = await cocotb.start(self._uart_rx_monitor(queue, bit_cycles, not_ascii=True))
        tx_fork = await cocotb.start(self._uart_tx_monitor(queue, bit_cycles, not_ascii=True))

    async def _uart_rx_monitor(self, queue, bit_cycles, not_ascii=False):
        while True:
            char = ""
            await FallingEdge(self.wb_uart_rx_hdl)  # start of char
            await ClockCycles(self.clk, bit_cycles+1)
            await NextTimeStep()
            for i in range(8):
                char = self.wb_uart_rx_hdl.value.binstr + char
                await ClockCycles(self.clk, bit_cycles+1)
                await NextTimeStep()
            transaction = UART_Transaction(
                type="rx", char=chr(int(char, 2)) if not not_ascii else hex(int(char, 2)))
            queue.put_nowait(transaction)
            cocotb.log.debug(f"[{__class__.__name__}][_soc_uart_rx_monitor] sending transaction {transaction} to queue")

    async def _uart_tx_monitor(self, queue, bit_cycles, not_ascii=False):
        while True:
            char = ""
            await FallingEdge(self.wb_uart_tx_hdl)
            await ClockCycles(self.clk, bit_cycles)
            for i in range(8):
                char = self.wb_uart_tx_hdl.value.binstr + char
                await ClockCycles(self.clk, bit_cycles)
            transaction = UART_Transaction(
                type="tx", char=chr(int(char, 2)) if not not_ascii else hex(int(char, 2)))
            queue.put_nowait(transaction)
            cocotb.log.debug(f"[{__class__.__name__}][_soc_uart_tx_monitor] sending transaction {transaction} to queue")
        
    def apb_hdls(self):
        self.clk_hdl = self.uart_hdl.PCLK
        self.reset_hdl = self.uart_hdl.PRESETn
        self.addr_hdl = self.uart_hdl.PADDR
        self.en_hdl = self.uart_hdl.PENABLE
        self.wdata_hdl = self.uart_hdl.PWDATA
        self.wen_hdl = self.uart_hdl.PWRITE
        self.rdata_hdl = self.uart_hdl.PRDATA
        self.ack_hdl = self.uart_hdl.PREADY
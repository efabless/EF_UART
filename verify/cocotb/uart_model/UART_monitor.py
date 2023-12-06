import cocotb
from cocotb.triggers import Timer, RisingEdge, ClockCycles, FallingEdge, NextTimeStep, Edge
from collections import namedtuple


UART_Transaction = namedtuple("UART_Transaction", ["type", "char", "prescale"])


class UART_apbMonitor:
    def __init__(self, hdl, queue, ip_regs_dict):
        self.uart_hdl = hdl
        self.ip_regs_dict = ip_regs_dict
        self._queue_fork = cocotb.scheduler.add(self._soc_uart_monitor(queue))
        cocotb.log.debug("[TEST] Start UART APB Monitor")

    async def update_bit_cycles(self):
        while True:
            self.bit_cycles = round((self.ip_regs_dict[8]["val"] + 1) * 16) +1
            cocotb.log.debug(f"[{__class__.__name__}] bit_cycles: {self.bit_cycles}")
            await ClockCycles(self.clk, 1)

    async def _soc_uart_monitor(self, queue):
        self.hdls()
        await cocotb.start(self.update_bit_cycles())
        cocotb.log.debug(f"[{__class__.__name__}][_soc_uart_monitor] bit_cycles: {self.bit_cycles}")
        rx_fork = await cocotb.start(self._soc_uart_rx_monitor(queue))
        tx_fork = await cocotb.start(self._soc_uart_tx_monitor(queue))

    async def _soc_uart_rx_monitor(self, queue, not_ascii=False):
        while True:
            char = ""
            await FallingEdge(self.rx_hdl)  # start of char
            await ClockCycles(self.clk, self.bit_cycles+1)
            await NextTimeStep()
            for i in range(8):
                char = self.rx_hdl.value.binstr + char
                await ClockCycles(self.clk, self.bit_cycles+1)
                await NextTimeStep()
            transaction = UART_Transaction(
                type="rx", char=chr(int(char, 2)) if not not_ascii else hex(int(char, 2)), prescale=self.ip_regs_dict[8]["val"])
            queue.put_nowait(transaction)
            cocotb.log.debug(f"[{__class__.__name__}][_soc_uart_rx_monitor] sending transaction {transaction} to queue")

    async def _soc_uart_tx_monitor(self, queue, not_ascii=False):
        while True:
            char = ""
            await FallingEdge(self.tx_hdl)
            await ClockCycles(self.clk, self.bit_cycles)
            for i in range(8):
                char = self.tx_hdl.value.binstr + char
                await ClockCycles(self.clk, self.bit_cycles)
            transaction = UART_Transaction(
                type="tx", char=chr(int(char, 2)) if not not_ascii else hex(int(char, 2)), prescale=self.ip_regs_dict[8]["val"])
            queue.put_nowait(transaction)
            cocotb.log.debug(f"[{__class__.__name__}][_soc_uart_tx_monitor] sending transaction {transaction} to queue")

    def hdls(self):
        self.clk = self.uart_hdl.PCLK
        self.rx_hdl = self.uart_hdl.RX
        self.tx_hdl = self.uart_hdl.TX

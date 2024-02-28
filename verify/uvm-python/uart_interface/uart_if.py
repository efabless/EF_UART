from uvm.base.sv import sv_if


class uart_if(sv_if):

    #  // Actual Signals
    # wire 		RX;
    # wire 		TX;

    def __init__(self, dut):
        bus_map = {"PCLK": "CLK", "PRESETn": "RESETn", "RX": "RX", "TX": "TX", "tx_done": "tx_done", "rx_done": "rx_done"}
        super().__init__(dut, "", bus_map)

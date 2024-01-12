from uvm.base.sv import sv_if


class wrapper_bus_if(sv_if):

    #  // Actual Signals
    # wire 		PCLK;
    # wire 		PRESETn;
    # wire [31:0]	PADDR;
    # wire 		PWRITE;
    # wire 		PSEL;
    # wire 		PENABLE;
    # wire [31:0]	PWDATA;
    # wire [31:0]	PRDATA;
    # wire 		PREADY;
    # wire 		irq;

    def __init__(self, dut):
        bus_map = {"PCLK": "PCLK", "PRESETn": "PRESETn", "PADDR": "PADDR", "PWRITE": "PWRITE", "PSEL": "PSEL", "PENABLE": "PENABLE", "PWDATA": "PWDATA", "PRDATA": "PRDATA", "PREADY": "PREADY"}
        sv_if.__init__(self, dut, "", bus_map)

class wrapper_irq_if(sv_if):

    #  // Actual Signals
    # wire 		irq;

    def __init__(self, dut):
        bus_map = {"irq": "irq"}
        sv_if.__init__(self, dut, "", bus_map)

`timescale 1ns/1ps

module top();
    reg 		CLK = 0;
    wire 		RESETn = 1;
    `ifdef BUS_TYPE_APB
        wire 		RX;
        wire 		TX;
       
        wire [31:0]	PADDR;
        wire 		PWRITE;
        wire 		PSEL;
        wire 		PENABLE;
        wire [31:0]	PWDATA;
        wire [31:0]	PRDATA;
        wire 		PREADY;
        wire 		irq;
        EF_UART_APB dut(.rx(RX), .tx(TX), .PCLK(CLK), .PRESETn(RESETn), .PADDR(PADDR), .PWRITE(PWRITE), .PSEL(PSEL), .PENABLE(PENABLE), .PWDATA(PWDATA), .PRDATA(PRDATA), .PREADY(PREADY), .IRQ(irq));
    `endif
    `ifdef BUS_TYPE_AHB
        wire [31:0]	HADDR;
        wire 		HWRITE;
        wire 		HSEL = 0;
        wire 		HREADYOUT;
        wire [1:0]	HTRANS=0;
        wire [31:0]	HWDATA;
        wire [31:0]	HRDATA;
        wire 		HREADY;
        wire 		irq;
        EF_UART_AHBL dut(.rx(RX), .tx(TX), .HCLK(CLK), .HRESETn(RESETn), .HADDR(HADDR), .HWRITE(HWRITE), .HSEL(HSEL), .HTRANS(HTRANS), .HWDATA(HWDATA), .HRDATA(HRDATA), .HREADY(HREADY),.HREADYOUT(HREADYOUT), .IRQ(irq));
    `endif
    // monitor inside signals
    wire tx_done = dut.instance_to_wrap.tx_done;
    wire rx_done = dut.instance_to_wrap.rx_done;

    `ifndef SKIP_WAVE_DUMP
        initial begin
            $dumpfile ({"waves.vcd"});
            $dumpvars(0, top);
        end
    `endif
    always #10 CLK = !CLK; // clk generator
endmodule
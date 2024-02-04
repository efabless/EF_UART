`timescale 1ns/1ps

module top();
    wire x=0;
    wire y=1;
    wire z;
    assign z = x+y;
    wire 		RX;
	wire 		TX;
	reg 		PCLK = 0;
	wire 		PRESETn = 1;
	wire [31:0]	PADDR;
	wire 		PWRITE;
	wire 		PSEL;
	wire 		PENABLE;
	wire [31:0]	PWDATA;
	wire [31:0]	PRDATA;
	wire 		PREADY;
	wire 		irq;
     // monitor inside signals
    wire tx_done = dut.instance_to_wrap.tx_done;
    wire rx_done = dut.instance_to_wrap.rx_done;
    EF_UART_APB dut(.rx(RX), .tx(TX), .PCLK(PCLK), .PRESETn(PRESETn), .PADDR(PADDR), .PWRITE(PWRITE), .PSEL(PSEL), .PENABLE(PENABLE), .PWDATA(PWDATA), .PRDATA(PRDATA), .PREADY(PREADY), .IRQ(irq));
    initial begin
        $dumpfile ({"waves.vcd"});
        $dumpvars(0, top);
    end
    always #10 PCLK = !PCLK; // clk generator
endmodule
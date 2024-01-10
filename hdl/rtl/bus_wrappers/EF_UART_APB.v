/*
	Copyright 2022 AUCOHL

	Author: Mohamed Shalan (mshalan@aucegypt.edu)

	Permission is hereby granted, free of charge, to any person obtaining
	a copy of this software and associated documentation files (the
	"Software"), to deal in the Software without restriction, including
	without limitation the rights to use, copy, modify, merge, publish,
	distribute, sublicense, and/or sell copies of the Software, and to
	permit persons to whom the Software is furnished to do so, subject to
	the following conditions:

	The above copyright notice and this permission notice shall be
	included in all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
	MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
	NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
	LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
	OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
	WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*/

/* THIS FILE IS GENERATED, DO NOT EDIT */

`timescale			1ns/1ps
`default_nettype		none

`define				APB_AW			16

`include			"apb_wrapper.vh"

module EF_UART_APB #( 
	parameter	
				SC = 8,
				MDW = 9,
				GFLEN = 8,
				FAW = 4
)(
	`APB_SLAVE_PORTS,
	input	[0:0]	rx,
	output	[0:0]	tx
);

	localparam	rxdata_REG_OFFSET = `APB_AW'd0;
	localparam	txdata_REG_OFFSET = `APB_AW'd4;
	localparam	prescaler_REG_OFFSET = `APB_AW'd12;
	localparam	control_REG_OFFSET = `APB_AW'd8;
	localparam	config_REG_OFFSET = `APB_AW'd16;
	localparam	fifo_control_REG_OFFSET = `APB_AW'd20;
	localparam	fifo_status_REG_OFFSET = `APB_AW'd24;
	localparam	match_REG_OFFSET = `APB_AW'd28;
	localparam	IM_REG_OFFSET = `APB_AW'd3840;
	localparam	MIS_REG_OFFSET = `APB_AW'd3844;
	localparam	RIS_REG_OFFSET = `APB_AW'd3848;
	localparam	IC_REG_OFFSET = `APB_AW'd3852;

	wire		clk = PCLK;
	wire		rst_n = PRESETn;


	`APB_CTRL_SIGNALS

	wire [16-1:0]	prescaler;
	wire [1-1:0]	en;
	wire [1-1:0]	tx_en;
	wire [1-1:0]	rx_en;
	wire [MDW-1:0]	wdata;
	wire [6-1:0]	timeout_bits;
	wire [1-1:0]	loopback_en;
	wire [1-1:0]	glitch_filter_en;
	wire [FAW-1:0]	tx_level;
	wire [FAW-1:0]	rx_level;
	wire [1-1:0]	rd;
	wire [1-1:0]	wr;
	wire [4-1:0]	data_size;
	wire [1-1:0]	stop_bits_count;
	wire [3-1:0]	parity_type;
	wire [FAW-1:0]	txfifotr;
	wire [FAW-1:0]	rxfifotr;
	wire [MDW-1:0]	match_data;
	wire [1-1:0]	tx_empty;
	wire [1-1:0]	tx_full;
	wire [1-1:0]	tx_level_below;
	wire [MDW-1:0]	rdata;
	wire [1-1:0]	rx_empty;
	wire [1-1:0]	rx_full;
	wire [1-1:0]	rx_level_above;
	wire [1-1:0]	break_flag;
	wire [1-1:0]	match_flag;
	wire [1-1:0]	frame_error_flag;
	wire [1-1:0]	parity_error_flag;
	wire [1-1:0]	overrun_flag;
	wire [1-1:0]	timeout_flag;


	wire	[MDW-1:0]	rxdata_WIRE;

	wire	[MDW-1:0]	txdata_WIRE;

	reg [16-1:0]	prescaler_REG;
	assign	prescaler = prescaler_REG;
	`APB_REG(prescaler_REG, 0, 16)

	reg [5-1:0]	control_REG;
	assign	en	=	control_REG[0 : 0];
	assign	tx_en	=	control_REG[1 : 1];
	assign	rx_en	=	control_REG[2 : 2];
	assign	loopback_en	=	control_REG[3 : 3];
	assign	glitch_filter_en	=	control_REG[4 : 4];
	`APB_REG(control_REG, 0, 5)

	reg [14-1:0]	config_REG;
	assign	data_size	=	config_REG[3 : 0];
	assign	stop_bits_count	=	config_REG[4 : 4];
	assign	parity_type	=	config_REG[7 : 5];
	assign	timeout_bits	=	config_REG[13 : 8];
	`APB_REG(config_REG, 'h3F08, 14)

	reg [16-1:0]	fifo_control_REG;
	assign	txfifotr	=	fifo_control_REG[(FAW - 1) : 0];
	assign	rxfifotr	=	fifo_control_REG[(FAW + 7) : 8];
	`APB_REG(fifo_control_REG, 0, 16)

	wire [16-1:0]	fifo_status_WIRE;
	assign	fifo_status_WIRE[(FAW - 1) : 0] = rx_level;
	assign	fifo_status_WIRE[(FAW + 7) : 8] = tx_level;

	reg [MDW-1:0]	match_REG;
	assign	match_data = match_REG;
	`APB_REG(match_REG, 0, MDW)

	reg [9:0] IM_REG;
	reg [9:0] IC_REG;
	reg [9:0] RIS_REG;

	`APB_MIS_REG(10)
	`APB_REG(IM_REG, 0, 10)
	`APB_IC_REG(10)

	wire [0:0] line_break = break_flag;
	wire [0:0] match = match_flag;
	wire [0:0] frame_error = frame_error_flag;
	wire [0:0] parity_error = parity_error_flag;
	wire [0:0] overrun = overrun_flag;
	wire [0:0] timeout = timeout_flag;


	integer _i_;
	`APB_BLOCK(RIS_REG, 0) else begin
		for(_i_ = 0; _i_ < 1; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(tx_empty[_i_ - 0] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 1; _i_ < 2; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(rx_full[_i_ - 1] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 2; _i_ < 3; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(tx_level_below[_i_ - 2] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 3; _i_ < 4; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(rx_level_above[_i_ - 3] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 4; _i_ < 5; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(line_break[_i_ - 4] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 5; _i_ < 6; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(match[_i_ - 5] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 6; _i_ < 7; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(frame_error[_i_ - 6] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 7; _i_ < 8; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(parity_error[_i_ - 7] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 8; _i_ < 9; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(overrun[_i_ - 8] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 9; _i_ < 10; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(timeout[_i_ - 9] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
	end

	assign IRQ = |MIS_REG;

	EF_UART #(
		.SC(SC),
		.MDW(MDW),
		.GFLEN(GFLEN),
		.FAW(FAW)
	) instance_to_wrap (
		.clk(clk),
		.rst_n(rst_n),
		.prescaler(prescaler),
		.en(en),
		.tx_en(tx_en),
		.rx_en(rx_en),
		.wdata(wdata),
		.timeout_bits(timeout_bits),
		.loopback_en(loopback_en),
		.glitch_filter_en(glitch_filter_en),
		.tx_level(tx_level),
		.rx_level(rx_level),
		.rd(rd),
		.wr(wr),
		.data_size(data_size),
		.stop_bits_count(stop_bits_count),
		.parity_type(parity_type),
		.txfifotr(txfifotr),
		.rxfifotr(rxfifotr),
		.match_data(match_data),
		.tx_empty(tx_empty),
		.tx_full(tx_full),
		.tx_level_below(tx_level_below),
		.rdata(rdata),
		.rx_empty(rx_empty),
		.rx_full(rx_full),
		.rx_level_above(rx_level_above),
		.break_flag(break_flag),
		.match_flag(match_flag),
		.frame_error_flag(frame_error_flag),
		.parity_error_flag(parity_error_flag),
		.overrun_flag(overrun_flag),
		.timeout_flag(timeout_flag),
		.rx(rx),
		.tx(tx)
	);

	assign	PRDATA = 
			(PADDR[`APB_AW-1:0] == rxdata_REG_OFFSET)	? rxdata_WIRE :
			(PADDR[`APB_AW-1:0] == txdata_REG_OFFSET)	? txdata_WIRE :
			(PADDR[`APB_AW-1:0] == prescaler_REG_OFFSET)	? prescaler_REG :
			(PADDR[`APB_AW-1:0] == control_REG_OFFSET)	? control_REG :
			(PADDR[`APB_AW-1:0] == config_REG_OFFSET)	? config_REG :
			(PADDR[`APB_AW-1:0] == fifo_control_REG_OFFSET)	? fifo_control_REG :
			(PADDR[`APB_AW-1:0] == fifo_status_REG_OFFSET)	? fifo_status_WIRE :
			(PADDR[`APB_AW-1:0] == match_REG_OFFSET)	? match_REG :
			(PADDR[`APB_AW-1:0] == IM_REG_OFFSET)	? IM_REG :
			(PADDR[`APB_AW-1:0] == MIS_REG_OFFSET)	? MIS_REG :
			(PADDR[`APB_AW-1:0] == RIS_REG_OFFSET)	? RIS_REG :
			(PADDR[`APB_AW-1:0] == IC_REG_OFFSET)	? IC_REG :
			32'hDEADBEEF;

	assign PREADY = 1'b1;

	assign	rxdata_WIRE = rdata;
	assign	rd = (apb_re & (PADDR[`APB_AW-1:0] == rxdata_REG_OFFSET));
	assign	wdata = PWDATA;
	assign	wr = (apb_we & (PADDR[`APB_AW-1:0] == txdata_REG_OFFSET));
endmodule

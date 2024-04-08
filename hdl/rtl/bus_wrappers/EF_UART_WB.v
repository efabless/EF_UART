/*
	Copyright 2024 Efabless Corp.

	Author: Mohamed Shalan (mshalan@efabless.com)

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	    http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.

*/

/* THIS FILE IS GENERATED, DO NOT EDIT */

`timescale			1ns/1ps
`default_nettype	none

`define				WB_AW		16

`include			"wb_wrapper.vh"

module EF_UART_WB #( 
	parameter	
		SC = 8,
		MDW = 9,
		GFLEN = 8,
		FAW = 4
) (
	`WB_SLAVE_PORTS,
	input	[0:0]	rx,
	output	[0:0]	tx
);

	localparam	RXDATA_REG_OFFSET = `WB_AW'd0;
	localparam	TXDATA_REG_OFFSET = `WB_AW'd4;
	localparam	PR_REG_OFFSET = `WB_AW'd8;
	localparam	CTRL_REG_OFFSET = `WB_AW'd12;
	localparam	CFG_REG_OFFSET = `WB_AW'd16;
	localparam	FIFOCTRL_REG_OFFSET = `WB_AW'd20;
	localparam	FIFOS_REG_OFFSET = `WB_AW'd24;
	localparam	MATCH_REG_OFFSET = `WB_AW'd28;
	localparam	IM_REG_OFFSET = `WB_AW'd3840;
	localparam	MIS_REG_OFFSET = `WB_AW'd3844;
	localparam	RIS_REG_OFFSET = `WB_AW'd3848;
	localparam	IC_REG_OFFSET = `WB_AW'd3852;

	wire		clk = clk_i;
	wire		rst_n = (~rst_i);


	`WB_CTRL_SIGNALS

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

	wire	[MDW-1:0]	RXDATA_WIRE;

	wire	[MDW-1:0]	TXDATA_WIRE;

	reg [16-1:0]	PR_REG;
	assign	prescaler = PR_REG;
	`WB_REG(PR_REG, 0, 16)

	reg [5-1:0]	CTRL_REG;
	assign	en	=	CTRL_REG[0 : 0];
	assign	tx_en	=	CTRL_REG[1 : 1];
	assign	rx_en	=	CTRL_REG[2 : 2];
	assign	loopback_en	=	CTRL_REG[3 : 3];
	assign	glitch_filter_en	=	CTRL_REG[4 : 4];
	`WB_REG(CTRL_REG, 0, 5)

	reg [14-1:0]	CFG_REG;
	assign	data_size	=	CFG_REG[3 : 0];
	assign	stop_bits_count	=	CFG_REG[4 : 4];
	assign	parity_type	=	CFG_REG[7 : 5];
	assign	timeout_bits	=	CFG_REG[13 : 8];
	`WB_REG(CFG_REG, 'h3F08, 14)

	reg [16-1:0]	FIFOCTRL_REG;
	assign	txfifotr	=	FIFOCTRL_REG[(FAW - 1) : 0];
	assign	rxfifotr	=	FIFOCTRL_REG[(FAW + 7) : 8];
	`WB_REG(FIFOCTRL_REG, 0, 16)

	wire [16-1:0]	FIFOS_WIRE;
	assign	FIFOS_WIRE[(FAW - 1) : 0] = rx_level;
	assign	FIFOS_WIRE[(FAW + 7) : 8] = tx_level;

	reg [MDW-1:0]	MATCH_REG;
	assign	match_data = MATCH_REG;
	`WB_REG(MATCH_REG, 0, MDW)

	reg [9:0] IM_REG;
	reg [9:0] IC_REG;
	reg [9:0] RIS_REG;

	`WB_MIS_REG(10)
	`WB_REG(IM_REG, 0, 10)
	`WB_IC_REG(10)

	wire [0:0] TXE = tx_empty;
	wire [0:0] RXF = rx_full;
	wire [0:0] TXB = tx_level_below;
	wire [0:0] RXA = rx_level_above;
	wire [0:0] BRK = break_flag;
	wire [0:0] MATCH = match_flag;
	wire [0:0] FE = frame_error_flag;
	wire [0:0] PRE = parity_error_flag;
	wire [0:0] OR = overrun_flag;
	wire [0:0] RTO = timeout_flag;


	integer _i_;
	`WB_BLOCK(RIS_REG, 0) else begin
		for(_i_ = 0; _i_ < 1; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(TXE[_i_ - 0] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 1; _i_ < 2; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(RXF[_i_ - 1] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 2; _i_ < 3; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(TXB[_i_ - 2] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 3; _i_ < 4; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(RXA[_i_ - 3] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 4; _i_ < 5; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(BRK[_i_ - 4] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 5; _i_ < 6; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(MATCH[_i_ - 5] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 6; _i_ < 7; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(FE[_i_ - 6] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 7; _i_ < 8; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(PRE[_i_ - 7] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 8; _i_ < 9; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(OR[_i_ - 8] == 1'b1) RIS_REG[_i_] <= 1'b1;
		end
		for(_i_ = 9; _i_ < 10; _i_ = _i_ + 1) begin
			if(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if(RTO[_i_ - 9] == 1'b1) RIS_REG[_i_] <= 1'b1;
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

	assign	dat_o = 
			(adr_i[`WB_AW-1:0] == RXDATA_REG_OFFSET)	? RXDATA_WIRE :
			(adr_i[`WB_AW-1:0] == TXDATA_REG_OFFSET)	? TXDATA_WIRE :
			(adr_i[`WB_AW-1:0] == PR_REG_OFFSET)	? PR_REG :
			(adr_i[`WB_AW-1:0] == CTRL_REG_OFFSET)	? CTRL_REG :
			(adr_i[`WB_AW-1:0] == CFG_REG_OFFSET)	? CFG_REG :
			(adr_i[`WB_AW-1:0] == FIFOCTRL_REG_OFFSET)	? FIFOCTRL_REG :
			(adr_i[`WB_AW-1:0] == FIFOS_REG_OFFSET)	? FIFOS_WIRE :
			(adr_i[`WB_AW-1:0] == MATCH_REG_OFFSET)	? MATCH_REG :
			(adr_i[`WB_AW-1:0] == IM_REG_OFFSET)	? IM_REG :
			(adr_i[`WB_AW-1:0] == MIS_REG_OFFSET)	? MIS_REG :
			(adr_i[`WB_AW-1:0] == RIS_REG_OFFSET)	? RIS_REG :
			(adr_i[`WB_AW-1:0] == IC_REG_OFFSET)	? IC_REG :
			32'hDEADBEEF;

	always @ (posedge clk_i or posedge rst_i)
		if(rst_i)
			ack_o <= 1'b0;
		else if(wb_valid & ~ack_o)
			ack_o <= 1'b1;
		else
			ack_o <= 1'b0;
	assign	RXDATA_WIRE = rdata;
	assign	rd =  ack_o & (wb_re & (adr_i[`WB_AW-1:0] == RXDATA_REG_OFFSET));
	assign	wdata = dat_i;
	assign	wr = ack_o & (wb_we & (adr_i[`WB_AW-1:0] == TXDATA_REG_OFFSET));
endmodule

/*
	Copyright 2020 AUCOHL

    Author: Mohamed Shalan (mshalan@aucegypt.edu)
	
	Licensed under the Apache License, Version 2.0 (the "License"); 
	you may not use this file except in compliance with the License. 
	You may obtain a copy of the License at:

	http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software 
	distributed under the License is distributed on an "AS IS" BASIS, 
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
	See the License for the specific language governing permissions and 
	limitations under the License.
*/

`timescale			    1ns/1ps
`default_nettype		none

`define     PED(clk, sig, pulse)    reg last_``sig``; always @(posedge clk) last_``sig`` <= sig; assign pulse = sig & ~last_``sig``;
`define     NED(clk, sig, pulse)    reg last_``sig``; always @(posedge clk) last_``sig`` <= sig; assign pulse = ~sig & last_``sig``;

/*
    Brute-force Synchronizer
*/
module aucohl_sync #(parameter NUM_STAGES = 2) (
    input clk,
    input in,
    output out
);

    reg [NUM_STAGES-1:0] sync;

    always @(posedge clk)
        sync <= {sync[NUM_STAGES-2:0], in};

    assign out = sync[NUM_STAGES-1];

endmodule

/*
    A positive edge detector
*/
module aucohl_ped (
    input clk,
    input in,
    output out
);
    `PED(clk, in, out)
endmodule

/*
    A negative edge detector
*/
module aucohl_ned (
    input clk,
    input in,
    output out
);
    `NED(clk, in, out)
endmodule

/*
    A tick generator
*/
module aucohl_ticker #(parameter W=8) (
    input   wire            clk, 
    input   wire            rst_n,
    input   wire            en,
    input   wire [W-1:0]    clk_div,
    output  wire            tick
);

    reg [W-1:0] counter;
    wire        counter_is_zero = (counter == 'b0);
    wire        tick_w;
    reg         tick_reg;

    always @(posedge clk, negedge rst_n)
        if(~rst_n)
            counter <=  'b0;
        else if(en) 
            if(counter_is_zero)
                counter <=  clk_div;
            else
                counter <=  counter - 'b1; 

    assign tick_w = (clk_div == 'b1)  ?   1'b1 : counter_is_zero;

    always @(posedge clk or negedge rst_n)
        if(!rst_n)
            tick_reg <= 1'b0;
        else if(en)
            tick_reg <= tick_w;
        else
            tick_reg <= 0;

    assign tick = tick_reg;

endmodule

/*
    A glitch filter
*/
module aucohl_glitch_filter #(parameter N = 8, CLKDIV = 1) (
    input   wire    clk,
    input   wire    rst_n,
    input   wire    in,
    output  reg     out
);

    reg [N-1:0] shifter;
    wire        tick;

    aucohl_ticker ticker (
        .clk(clk),
        .rst_n(rst_n),
        .en(1'b1),
        .clk_div(CLKDIV),
        .tick(tick)
    );

    always @(posedge clk, negedge rst_n)
        if(!rst_n)
            shifter = 'b0;
        else if(tick)
            shifter <= {shifter[N-2:0], in};

    wire all_ones   = & shifter;
    wire all_zeros  = ~| shifter;

    always @(posedge clk, negedge rst_n)
        if(!rst_n)
            out <= 1'b0;
        else
            if(all_ones) 
                out <= 1'b1;
            else if(all_zeros) 
                out <= 1'b0;
endmodule

/*
    A FIFO
*/
module aucohl_fifo #(parameter DW=8, AW=4)(
    input     wire            clk,
    input     wire            rst_n,
    input     wire            rd,
    input     wire            wr,
    input     wire [DW-1:0]   wdata,
    output    wire            empty,
    output    wire            full,
    output    wire [DW-1:0]   rdata,
    output    wire [AW-1:0]   level    
);

    localparam  DEPTH = 2**AW;

    //Internal Signal declarations
    reg [DW-1:0]  array_reg [DEPTH-1:0];
    reg [AW-1:0]  w_ptr_reg;
    reg [AW-1:0]  w_ptr_next;
    reg [AW-1:0]  w_ptr_succ;
    reg [AW-1:0]  r_ptr_reg;
    reg [AW-1:0]  r_ptr_next;
    reg [AW-1:0]  r_ptr_succ;
    // array reg 
    wire[DW-1:0] array_reg_0 = array_reg[0];
    wire[DW-1:0] array_reg_1 = array_reg[1];
    wire[DW-1:0] array_reg_2 = array_reg[2];
    wire[DW-1:0] array_reg_3 = array_reg[3];
    wire[DW-1:0] array_reg_4 = array_reg[4];
    wire[DW-1:0] array_reg_5 = array_reg[5];
    wire[DW-1:0] array_reg_6 = array_reg[6];
    wire[DW-1:0] array_reg_7 = array_reg[7];
    wire[DW-1:0] array_reg_8 = array_reg[8];
    wire[DW-1:0] array_reg_9 = array_reg[9];
    wire[DW-1:0] array_reg_10 = array_reg[10];
    wire[DW-1:0] array_reg_11 = array_reg[11];
    wire[DW-1:0] array_reg_12 = array_reg[12];
    wire[DW-1:0] array_reg_13 = array_reg[13];
    wire[DW-1:0] array_reg_14 = array_reg[14];
    wire[DW-1:0] array_reg_15 = array_reg[15];
    
    // Level
    reg [AW-1:0] level_reg;
    reg [AW-1:0] level_next;      
    reg full_reg;
    reg empty_reg;
    reg full_next;
    reg empty_next;

    wire w_en;

    always @ (posedge clk)
        if(w_en) begin
            array_reg[w_ptr_reg] <= wdata;
        end

    assign rdata = array_reg[r_ptr_reg];   
    assign w_en = wr & ~full_reg;           

    //State Machine
    always @ (posedge clk, negedge rst_n) begin 
    if(!rst_n)
        begin
            w_ptr_reg <= 'b0;
            r_ptr_reg <= 'b0;
            full_reg  <= 1'b0;
            empty_reg <= 1'b1;
            level_reg <= 4'd0;
        end
    else
        begin
            w_ptr_reg <= w_ptr_next;
            r_ptr_reg <= r_ptr_next;
            full_reg  <= full_next;
            empty_reg <= empty_next;
            level_reg <= level_next;
        end
    end

    //Next State Logic
    always @* begin
        w_ptr_succ = w_ptr_reg + 1;
        r_ptr_succ = r_ptr_reg + 1;

        w_ptr_next = w_ptr_reg;
        r_ptr_next = r_ptr_reg;
        full_next = full_reg;
        empty_next = empty_reg;
        level_next = level_reg;

        case({w_en,rd})
            //2'b00: nop
            2'b01: 
                if(~empty_reg) begin
                    r_ptr_next = r_ptr_succ;
                    full_next = 1'b0;
                    level_next = level_reg - 1;
                    if (r_ptr_succ == w_ptr_reg)
                        empty_next = 1'b1;
                end
            
            2'b10: 
                if(~full_reg) begin
                    w_ptr_next = w_ptr_succ;
                    empty_next = 1'b0;
                    level_next = level_reg + 1;
                    if (w_ptr_succ == r_ptr_reg)
                        full_next = 1'b1;
                end
            
            2'b11: begin
                w_ptr_next = w_ptr_succ;
                r_ptr_next = r_ptr_succ;
            end
        endcase
    end

    //Set Full and Empty
    assign full = full_reg;
    assign empty = empty_reg;
    assign level = level_reg;
  
endmodule

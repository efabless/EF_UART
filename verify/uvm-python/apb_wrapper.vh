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

`define		APB_BLOCK(name, init)		always @(posedge PCLK or negedge PRESETn) if(~PRESETn) name <= init;

`define     APB_CTRL_SIGNALS            wire		apb_valid   = PSEL & PENABLE;\
                                        wire		apb_we	    = PWRITE & apb_valid;\
                                        wire		apb_re	    = ~PWRITE & apb_valid;
                                        
`define		APB_REG(name, init, size)	`APB_BLOCK(name, init)\ 
                                        else if(apb_we & (PADDR[`APB_AW-1:0]==``name``_OFFSET))\ 
                                            name <= PWDATA[``size``-1:0];

`define		APB_IC_REG(size)			`APB_BLOCK(IC_REG, ``size``'b0)\
                                        else if(apb_we & (PADDR[`APB_AW-1:0]==IC_REG_OFFSET))\ 
                                            IC_REG <= PWDATA[``size``-1:0];\ 
                                        else \
                                            IC_REG <= ``size``'d0;    

`define     APB_SLAVE_PORTS             input wire          PCLK,\
                                        input wire          PRESETn,\
                                        input wire          PWRITE,\
                                        input wire [31:0]   PWDATA,\
                                        input wire [31:0]   PADDR,\
                                        input wire          PENABLE,\
                                        input wire          PSEL,\
                                        output wire         PREADY,\
                                        output wire [31:0]  PRDATA,\
                                        output wire         IRQ\
                                        
`define     APB_MIS_REG(size)           wire[size-1:0]      MIS_REG	= RIS_REG & IM_REG;
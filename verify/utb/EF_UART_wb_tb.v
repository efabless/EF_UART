/*
	Copyright 2020 Mohamed Shalan
	
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

`timescale          1ns/1ns

module EF_UART_apb_tb;

    `include "params.vh"
                
    reg         clk_i;
    reg         rst_i;
    reg [31:0]  adr_i;
    reg [31:0]  dat_i;
    wire[31:0]  dat_o;
    reg [3:0]   sel_i;
    reg         cyc_i;
    reg         stb_i;
    wire        ack_o;
    reg         we_i;

    wire        TX;
    wire        RX;
    wire        irq;

    `include "wb_tasks.vh"

    initial begin
        $dumpfile("EF_UART_wb_tb.vcd");
        $dumpvars;
        #2_500_000;
        $display("Timeout!"); 
        $finish;
    end

    event   e_reset, e_reset_done;
    event   e_test1, e_test1_done;

    // initializations & reset
    initial begin
        clk_i = 1'b0;
        rst_i = 1'bx;
        #55;
        -> e_reset;
        @(e_reset_done);
        -> e_test1;
        @(e_test1_done);
        $finish;
    end

    always #5 clk_i = !clk_i;

    // Reset
    always @(e_reset) begin
        rst_i <= 1'b1;
        #333;
        @(posedge clk_i);
        rst_i <= 1'b0;
        -> e_reset_done;
    end

    // Test 1
    reg [7:0] status=0, rx_data=0;
    initial begin
        @(e_test1);
        // Configure the prescales
        WB_M_WR_W(PRESCALE_REG_ADDR, 2);   
        WB_M_WR_W(CONTROL_REG_ADDR, 0);                // Disable the UART       
        WB_M_WR_W(IM_REG_ADDR, 0);                  // Disable all interrupts
        WB_M_WR_W(ICR_REG_ADDR, 8'hFF); 
        //WB_M_WR_W(TXFIFOTR_REG_ADDR, 4 );         // Set the TX FIFO threshold
        WB_M_WR_W(RXFIFOT_REG_ADDR, 7 );           // Set the TX FIFO threshold
        WB_M_WR_W(IM_REG_ADDR, IRQ_RX_FIFO_ABOVE);  // Enable RX FIFO Above Threshold Interrupt
        WB_M_WR_W(CONTROL_REG_ADDR, 7);                // Enable UART, TX and RX       
        
        // Send some data
        WB_M_WR_W(TXDATA_REG_ADDR, 8'h11);
        WB_M_WR_W(TXDATA_REG_ADDR, 8'h22);
        WB_M_WR_W(TXDATA_REG_ADDR, 8'h33);
        WB_M_WR_W(TXDATA_REG_ADDR, 8'h44);
        WB_M_WR_W(TXDATA_REG_ADDR, 8'h55);
        WB_M_WR_W(TXDATA_REG_ADDR, 8'h66);
        WB_M_WR_W(TXDATA_REG_ADDR, 8'h77);
        WB_M_WR_W(TXDATA_REG_ADDR, 8'h88);

        // wait for the first character to be received
        WB_M_RD_W(MIS_REG_ADDR, status);
        while ((status & IRQ_RX_FIFO_ABOVE) == 0) begin
            WB_M_RD_W(MIS_REG_ADDR, status);
        end
        $display("RX FIFO has 8 characters");  
        // Reading the 8 characters
        repeat(8) begin
            WB_M_RD_W(RXDATA_REG_ADDR, rx_data);
            $display("Received: 0x%x", rx_data);
        end
        -> e_test1_done;
	end

    EF_UART_wb MUV (
        //WB Interface
        .clk_i(clk_i),
        .rst_i(rst_i),
        .adr_i(adr_i),
        .dat_i(dat_i),
        .dat_o(dat_o),
        .sel_i(sel_i),
        .cyc_i(cyc_i),
        .stb_i(stb_i),
        .ack_o(ack_o),
        .we_i(we_i),

        .irq(irq),

        //Serial Port Signals
        .RX(RX),
        .TX(TX)
    );

    // Create a loopback!
    assign RX = TX;

endmodule

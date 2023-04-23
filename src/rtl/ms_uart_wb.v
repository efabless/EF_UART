/*
    Wishbone bus wrapper for the ms_uart IP
    Author: Mohamed Shalan (mshalan@aucegypt.edu)
    License: Apache 2.0
*/

`timescale          1ns/1ns
`default_nettype    none

`define     WB_REG(name, init_value,size)    always @(posedge clk_i or posedge rst_i) if(rst_i) name <= init_value; else if(wb_we & (adr_i[15:0]==``name``_ADDR)) name <= dat_i[size-1:0];

module ms_uart_wb (
    // WB bus Interface
    input   wire        clk_i,
    input   wire        rst_i,
    input   wire [31:0] adr_i,
    input   wire [31:0] dat_i,
    output  wire [31:0] dat_o,
    input   wire [3:0]  sel_i,
    input   wire        cyc_i,
    input   wire        stb_i,
    output  reg         ack_o,
    input   wire        we_i,

    input wire          RX,  
    output wire         TX,  

    output wire         irq 
);

    localparam  DATA_REG_ADDR       = 16'h0000,
                PRESCALE_REG_ADDR   = 16'h0004,
                TXFIFOTR_REG_ADDR   = 16'h0008,
                RXFIFOTR_REG_ADDR   = 16'h000c,
                CTRL_REG_ADDR       = 16'h0100,
                RIS_REG_ADDR        = 16'h0200,
                MIS_REG_ADDR        = 16'h0204,
                IM_REG_ADDR         = 16'h0208,
                ICR_REG_ADDR        = 16'h020C;

    //reg [ 7:0]  DATA_REG;
    reg [15:0]  PRESCALE_REG;
    reg [ 3:0]  TXFIFOTR_REG;
    reg [ 3:0]  RXFIFOTR_REG;
    reg [ 0:0]  CTRL_REG;
    reg [ 5:0]  IM_REG;
    reg [ 5:0]  ICR_REG;
    reg [ 5:0]  RIS_REG;
    
    wire [ 5:0] MIS_REG = RIS_REG & IM_REG;

    // WB Control Signals
    wire        wb_valid        =   cyc_i & stb_i;
    wire        wb_we           =   we_i & wb_valid;
    wire        wb_re           =   ~we_i & wb_valid;
    wire[3:0]   wb_byte_sel     =   sel_i & {4{wb_we}};

    wire [15:0] prescale        =   PRESCALE_REG[15:0];
    wire        en              =   CTRL_REG[0];
    wire        rd              =   wb_re & (adr_i[15:0] == DATA_REG_ADDR);
    wire        wr              =   wb_we & (adr_i[15:0] == DATA_REG_ADDR);
    wire [7:0]  wdata           =   dat_i[7:0];
    wire        tx_empty_flag;
    wire        tx_full_flag;
    wire [3:0]  tx_level;
    wire        tx_below_flag   =   (tx_level < TXFIFOTR_REG);
    wire [7:0]  rdata;
    wire        rx_empty_flag;
    wire        rx_full_flag;
    wire [3:0]  rx_level;
    wire        rx_above_flag   =   (rx_level > RXFIFOTR_REG);
   
    // RIS Register
    // bit 0: TX fifo is full Flag
    // bit 1: TX fifo is empty Flag
    // bit 2: TX fifo level is below threshold
    // bit 3: RX fifo is full Flag
    // bit 4: RX fifo is empty Flag
    // bit 5: RX fifo level is above threshold
    always @(posedge clk_i or posedge rst_i)
        if(rst_i)   
            RIS_REG <= 6'd0;
        else begin
            if(tx_full_flag)    
                RIS_REG[0] <= 1'b1;
            else if(ICR_REG[0])
                RIS_REG[0] <= 1'b0;
            
            if(tx_empty_flag)    
                RIS_REG[1] <= 1'b1;
            else if(ICR_REG[1])
                RIS_REG[1] <= 1'b0;

            if(tx_below_flag)    
                RIS_REG[2] <= 1'b1;
            else if(ICR_REG[2])
                RIS_REG[2] <= 1'b0;
            
            if(rx_full_flag)    
                RIS_REG[3] <= 1'b1;
            else if(ICR_REG[3])
                RIS_REG[3] <= 1'b0;
            
            if(rx_empty_flag)    
                RIS_REG[4] <= 1'b1;
            else if(ICR_REG[4])
                RIS_REG[4] <= 1'b0;

            if(rx_above_flag)    
                RIS_REG[5] <= 1'b1;
            else if(ICR_REG[5])
                RIS_REG[5] <= 1'b0;
        end

    // ICR Register
    // Writing to it clears the corresponding Interrupt flag
    // Automatically clears to 0 after writing to it
    always @(posedge clk_i or posedge rst_i)
        if(rst_i)   
            ICR_REG <= 6'b0;
        else
            if(wb_we & (adr_i[15:0] == ICR_REG_ADDR))
                ICR_REG <= dat_i[5:0];
            else
                ICR_REG <= 6'd0;

    //`APB_REG(DATA_REG, 32'd0, 7)
    `WB_REG(PRESCALE_REG, 32'd0, 16)
    `WB_REG(TXFIFOTR_REG, 32'd0, 4)
    `WB_REG(RXFIFOTR_REG, 32'd0, 4)
    `WB_REG(CTRL_REG, 32'd0, 1)            
    `WB_REG(IM_REG, 32'd0, 6)

    // WB Data out
    assign  dat_o   =   (PADDR[15:0] == DATA_REG_ADDR)      ?   rdata           :
                        (PADDR[15:0] == PRESCALE_REG_ADDR)  ?   PRESCALE_REG    :
                        (PADDR[15:0] == TXFIFOTR_REG_ADDR)  ?   TXFIFOTR_REG    :
                        (PADDR[15:0] == RXFIFOTR_REG_ADDR)  ?   RXFIFOTR_REG    :
                        (PADDR[15:0] == CTRL_REG_ADDR)      ?   CTRL_REG        :
                        (PADDR[15:0] == RIS_REG_ADDR)       ?   RIS_REG         :
                        (PADDR[15:0] == MIS_REG_ADDR)       ?   MIS_REG         :
                        (PADDR[15:0] == IM_REG_ADDR)        ?   IM_REG          :
                        (PADDR[15:0] == ICR_REG_ADDR)       ?   32'd0           :   32'hDEADBEEF;
                 
    assign irq = |MIS_REG;

    always @ (posedge clk_i or posedge rst_i)
        if(rst_i)
            ack_o <= 1'b0;
        else 
            if(wb_valid & ~ack_o)
                ack_o <= 1'b1;
            else
                ack_o <= 1'b0;

    ms_uart uart (
        .clk(clk_i),
        .rst_n(~rst_i),

        .prescale(PRESCALE_REG),
        .en(en),
        .rd(rd),
        .wr(wr),
        .wdata(wdata),
        .tx_empty(tx_empty_flag),
        .tx_full(tx_full_flag),
        .tx_level(tx_level),
        .rdata(rdata),
        .rx_empty(rx_empty_flag),
        .rx_full(rx_full_flag),
        .rx_level(rx_level),

        .RX(RX),
        .TX(TX)
    );

endmodule

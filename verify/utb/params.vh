    localparam[15:0] TXDATA_REG_ADDR = 16'h0000;
    localparam[15:0] RXDATA_REG_ADDR = 16'h0004;
    localparam[15:0] PRESCALE_REG_ADDR = 16'h0008;
    localparam[15:0] TXFIFOLEVEL_REG_ADDR = 16'h000c;
    localparam[15:0] RXFIFOLEVEL_REG_ADDR = 16'h0010;
    localparam[15:0] TXFIFOT_REG_ADDR = 16'h0014;
    localparam[15:0] RXFIFOT_REG_ADDR = 16'h0018;
    localparam[15:0] CONTROL_REG_ADDR = 16'h001c;
    localparam[15:0] ICR_REG_ADDR = 16'h0f00;
    localparam[15:0] RIS_REG_ADDR = 16'h0f04;
    localparam[15:0] IM_REG_ADDR = 16'h0f08;
    localparam[15:0] MIS_REG_ADDR = 16'h0f0c;

    localparam  IRQ_TX_FIFO_EMPTY   = 'h01,
                IRQ_TX_FIFO_BELOW   = 'h02,
                IRQ_RX_FIFO_FULL    = 'h04,
                IRQ_RX_FIFO_ABOVE   = 'h08;
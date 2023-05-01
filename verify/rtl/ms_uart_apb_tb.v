
module ms_uart_apb_tb;

    localparam  DATA_REG_ADDR       = 16'h0000,
                PRESCALE_REG_ADDR   = 16'h0004,
                TXFIFOTR_REG_ADDR   = 16'h0008,
                RXFIFOTR_REG_ADDR   = 16'h000c,
                CTRL_REG_ADDR       = 16'h0100,
                RIS_REG_ADDR        = 16'h0200,
                MIS_REG_ADDR        = 16'h0204,
                IM_REG_ADDR         = 16'h0208,
                ICR_REG_ADDR        = 16'h020C;

    localparam  IRQ_TX_FIFO_FULL    = 6'h01,
                IRQ_TX_FIFO_EMPTY   = 6'h02,
                IRQ_TX_FIFO_BELOW   = 6'h04,
                IRQ_RX_FIFO_FULL    = 6'h08,
                IRQ_RX_FIFO_EMPTY   = 6'h10,
                IRQ_RX_FIFO_ABOVE   = 6'h20;

    reg         PCLK;
    reg         PRESETn;
    reg         PWRITE;
    reg [31:0]  PWDATA;
    reg [31:0]  PADDR;
    reg         PENABLE;
    reg         PSEL;
    
    wire        PREADY;
    wire [31:0] PRDATA;


    //Serial Port Signals
    wire    RX;  //Input from RS-232
    wire    TX;  //Output to RS-232

    //UART Interrupt
    wire irq;  //Interrupt

    `include "apb_tasks.vh"

    initial begin
        $dumpfile("ms_uart_apb_tb.vcd");
        $dumpvars;
        #250_000;
        $display("Timeout!"); 
        $finish;
    end

    event   e_reset, e_reset_done;
    event   e_test1, e_test1_done;

    // initializations & reset
    initial begin
        PCLK = 1'b0;
        PRESETn = 1'bx;
        #55;
        -> e_reset;
        @(e_reset_done);
        -> e_test1;
        @(e_test1_done);
        $finish;
    end

    always #5 PCLK = !PCLK;

    
    // Reset
    always @(e_reset) begin
        PRESETn <= 1'b0;
        #333;
        @(posedge PCLK);
        PRESETn <= 1'b1;
        -> e_reset_done;
    end

    // Test 1
    reg [7:0] status=0, rx_data=0;
    initial begin
        @(e_test1);
        // Configure the prescales
        APB_M_WR(PRESCALE_REG_ADDR, 2);   
        APB_M_WR(CTRL_REG_ADDR, 0);                 // Disable the UART       
        APB_M_WR(IM_REG_ADDR, 0);                   // Disable all interrupts
        APB_M_WR(ICR_REG_ADDR, 8'hFF);
        //WB_M_WR_W(TXFIFOTR_REG_ADDR, 4 );         // Set the TX FIFO threshold
        APB_M_WR(RXFIFOTR_REG_ADDR, 7 );            // Set the TX FIFO threshold
        APB_M_WR(IM_REG_ADDR, IRQ_RX_FIFO_ABOVE); 
        APB_M_WR(CTRL_REG_ADDR, 7);                 // Enable UART, TX and RX
        // Send some data
        APB_M_WR(DATA_REG_ADDR, 8'h11);
        APB_M_WR(DATA_REG_ADDR, 8'h22);
        APB_M_WR(DATA_REG_ADDR, 8'h33);
        APB_M_WR(DATA_REG_ADDR, 8'h44);
        APB_M_WR(DATA_REG_ADDR, 8'h55);
        APB_M_WR(DATA_REG_ADDR, 8'h66);
        APB_M_WR(DATA_REG_ADDR, 8'h77);
        APB_M_WR(DATA_REG_ADDR, 8'h88);

        // wait for the first character to be received
        APB_M_RD(MIS_REG_ADDR, status);
        while ((status & IRQ_RX_FIFO_ABOVE) == 0) begin
            APB_M_RD(MIS_REG_ADDR, status);
        end
        $display("RX FIFO has 8 characters");  
        
        // Reading the 8 characters
        repeat(8) begin
            APB_M_RD(DATA_REG_ADDR, rx_data);
            $display("Received: 0x%x", rx_data);
        end
        -> e_test1_done;
	end

    ms_uart_apb MUV (
        //APB Interface
        .PCLK(PCLK),
        .PRESETn(PRESETn),
        .PWRITE(PWRITE),
        .PWDATA(PWDATA),
        .PADDR(PADDR),
        .PENABLE(PENABLE),
        .PSEL(PSEL),
        .PREADY(PREADY),
        .PRDATA(PRDATA),

        .irq(irq),

        //Serial Port Signals
        .RX(RX),
        .TX(TX)
    );

    // Create a loopback!
    assign RX = TX;

endmodule

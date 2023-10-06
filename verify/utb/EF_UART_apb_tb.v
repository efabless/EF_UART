
module EF_UART_apb_tb;

    `include "params.vh"

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
        $dumpfile("EF_UART_apb_tb.vcd");
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
        PADDR = 0;
        PWRITE = 0;
        PSEL = 0;
        PENABLE = 0;
        PWDATA = 0;
        #55;
        -> e_reset;
        @(e_reset_done);
        -> e_test1;
        @(e_test1_done);
        $finish;
    end

    always #10 PCLK = !PCLK;

    
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
        APB_M_WR(CONTROL_REG_ADDR, 0);                 // Disable the UART       
        APB_M_WR(IM_REG_ADDR, 0);                   // Disable all interrupts
        APB_M_WR(ICR_REG_ADDR, 8'hFF);
        //WB_M_WR_W(TXFIFOTR_REG_ADDR, 4 );         // Set the TX FIFO threshold
        APB_M_WR(RXFIFOT_REG_ADDR, 7 );            // Set the TX FIFO threshold
        APB_M_WR(IM_REG_ADDR, IRQ_RX_FIFO_ABOVE); 
        APB_M_WR(CONTROL_REG_ADDR, 7);                 // Enable UART, TX and RX
        // Send some data
        APB_M_WR(TXDATA_REG_ADDR, 8'h11);
        APB_M_WR(TXDATA_REG_ADDR, 8'h22);
        APB_M_WR(TXDATA_REG_ADDR, 8'h33);
        APB_M_WR(TXDATA_REG_ADDR, 8'h44);
        APB_M_WR(TXDATA_REG_ADDR, 8'h55);
        APB_M_WR(TXDATA_REG_ADDR, 8'h66);
        APB_M_WR(TXDATA_REG_ADDR, 8'h77);
        APB_M_WR(TXDATA_REG_ADDR, 8'h88);

        // wait for the first character to be received
        APB_M_RD(MIS_REG_ADDR, status);
        while ((status & IRQ_RX_FIFO_ABOVE) == 0) begin
            APB_M_RD(MIS_REG_ADDR, status);
        end
        $display("RX FIFO has 8 characters");  
        
        // Reading the 8 characters
        repeat(8) begin
            APB_M_RD(RXDATA_REG_ADDR, rx_data);
            $display("Received: 0x%x", rx_data);
        end
        -> e_test1_done;
	end

    EF_UART_apb MUV (
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

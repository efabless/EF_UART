`ifdef VERIFY

module ms_uart_apb_tb;

    reg PCLK;
    reg  PRESETn;
    reg  PWRITE;
    reg  [31:0] PWDATA;
    reg  [31:0] PADDR;
    reg  PENABLE;
    
    reg PSEL;
    
    //APB Outputs
     wire PREADY;
     wire [31:0] PRDATA;


    //Serial Port Signals
    wire         RsRx;  //Input from RS-232
    wire        RsTx;  //Output to RS-232

    //UART Interrupt
    wire uart_irq;  //Interrupt

    always #5 PCLK = !PCLK;

    initial begin
        $dumpfile("ms_uart_apb_tb.vcd");
        $dumpvars;
        # 25000 $finish;
    end

    initial begin
        PCLK = 0;
        PRESETn = 1;
		PSEL = 0;
		#10;
		@(posedge PCLK);
		PRESETn = 0;
		#100;
		@(posedge PCLK);
		PRESETn = 1;

        // Configure the prescales
        APB_WR(1, `PRESCALE_ADDR);
        APB_WR(1, `CTRL_ADDR);
        APB_WR(0, `IMASK_ADDR);
        APB_WR(6, `TXFIFOTR_ADDR );
        APB_WR(9, `IMASK_ADDR);
    
        // write something
        APB_WR(8'h7F, 0);
        APB_WR(8'h7F, 0);
        APB_WR(8'h7F, 0);
        APB_WR(8'h7F, 0);
        APB_WR(8'h7F, 0);
        APB_WR(8'h7F, 0);
        APB_WR(8'h7F, 0);
        APB_WR(8'h7F, 0);

        // wait for the first character to be received
        APB_RD(`STATUS_ADDR);
        while (PRDATA!=2) begin
            APB_RD(`STATUS_ADDR);
        end  

        // change the baud rate
        APB_WR(0, `CTRL_ADDR);
        APB_WR(4, `PRESCALE_ADDR);
        APB_WR(1, `CTRL_ADDR);
    
	end

    task APB_WR (input [31:0] data, input [31:0] address);
        begin
            @(posedge PCLK);
            PSEL = 1;
            PWRITE = 1;
            PWDATA = data;
            PENABLE = 0;
            PADDR = address;
            @(posedge PCLK);
            PENABLE = 1;
            @(posedge PCLK);
            PSEL = 0;
            PWRITE = 0;
            PENABLE = 0;
        end
    endtask
		
    task APB_RD(input [31:0] address);
			begin
				@(posedge PCLK);
				PSEL = 1;
				PWRITE = 0;
				PENABLE = 0;
                PADDR = address;
				@(posedge PCLK);
                PENABLE = 1;
				@(posedge PCLK);
				PSEL = 0;
				PWRITE = 0;
				PENABLE = 0;
			end
	endtask
	

    ms_uart_apb MUV (
        //APB Inputs
        PCLK,
        PRESETn,
        PWRITE,
        PWDATA,
        PADDR,
        PENABLE,
        PSEL,
    
        //APB Outputs
        PREADY,
        PRDATA,


        //Serial Port Signals
        RsRx,  //Input from RS-232
        RsTx,  //Output to RS-232

        //UART Interrupt
        uart_irq  //Interrupt
    );

assign RsRx = RsTx;

endmodule

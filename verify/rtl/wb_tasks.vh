task WB_M_WR_W(input [31:0] addr, input [31:0] data);
    begin : task_body
        @(posedge clk_i);
        #1;
        cyc_i <= 1;
        stb_i <= 1;
        we_i <= 1;
        adr_i <= addr;
        dat_i <= data;
        sel_i <= 4'hF;
        @(posedge ack_o);
        @(posedge clk_i);
        cyc_i <= 0;
        stb_i <= 0;
    end
endtask

task WB_M_RD_W(input [31:0] addr, output [31:0] data);
    begin : task_body
        @(posedge clk_i);
        #1;
        cyc_i <= 1;
        stb_i <= 1;
        we_i <= 0;
        adr_i <= addr;
        dat_i <= 0;
        sel_i <= 4'hF;
        @(posedge ack_o);
        @(posedge clk_i);
        data = dat_o;
        cyc_i = 0;
        stb_i = 0;
    end
endtask
/*
    Brute-force Synchronizer
*/
module aucohl_sync #(parameter NUM_STAGES = 2) (
    input wire clk,
    input wire in,
    output wire out
);

    reg [NUM_STAGES-1:0] sync;

    always @(posedge clk)
        sync <= {sync[NUM_STAGES-2:0], in};

    assign out = sync[NUM_STAGES-1];

endmodule
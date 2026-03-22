module button_debouncer#(
    parameter int CLK_FREQ = 100000000
    )(
    input logic clk, reset, btn,
    output logic level, tick
);

    localparam int sample_freq = 1000;
    localparam int sample_per = CLK_FREQ/sample_freq;
    localparam int count_width = (sample_per == 1) ? 1 : $clog2(sample_per);

    logic sync_btn;

    synchronizer btn_synchronizer(
        .clk(clk), 
        .btn(btn), 
        .sync_btn(sync_btn)
    );

    typedef enum logic [1:0] {
        zero,
        wait1,
        one,
        wait0
    } state_t;

    state_t PS, NS;
    logic [count_width-1:0] clk_count;

    always_comb begin
        NS = PS;
        unique case(PS) 
            zero: NS = (sync_btn) ? wait1 : zero;
            wait1: NS = (sync_btn) ? one : zero;
            one: NS = (sync_btn) ? one : wait0;
            wait0: NS = (sync_btn) ? one : zero;
            default: NS = zero;
        endcase
    end

    always_ff @(posedge clk) begin
        tick <= 1'b0;
        if(reset) begin
            PS <= zero;
            clk_count <= '0;
            tick <= 1'b0;
        end else if(clk_count == count_width'(sample_per-1)) begin
            if((NS == one) && (PS != one))
                tick <= 1'b1; 

            PS <= NS;
            clk_count <= '0;
        end else
            clk_count <= clk_count + 1;
    end

    assign level = (PS == one);

endmodule

module synchronizer(
    input logic clk, btn,
    output logic sync_btn
);

    logic sync0, sync1;

    always_ff @(posedge clk) begin 
        sync0 <= btn;
        sync1 <= sync0;
    end

    assign sync_btn = sync1;
    
endmodule


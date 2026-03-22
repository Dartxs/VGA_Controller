import vga_controller_pkg::*;

module char_selector(
    input logic clk, reset, next_tick, prev_tick,
    output logic [$clog2(CHAR_TOTAL)-1:0] char_select
);

    always_ff @(posedge clk, posedge reset) begin
        if(reset)
            char_select <= '0;
        else if(next_tick) begin
            if(char_select == $clog2(CHAR_TOTAL)'(CHAR_TOTAL-1))
                char_select <= '0;
            else
                char_select <= char_select + 1;
        end else if(prev_tick) begin
                if(char_select == 0) 
                    char_select <= $clog2(CHAR_TOTAL)'(CHAR_TOTAL-1);
                else
                    char_select <= char_select - 1;
        end
    end

endmodule



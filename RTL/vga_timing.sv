/*

Module for managing Hsync, Vsync, and video_on timings

*/

module vga_timing(
    input logic clk, areset,
    output logic Hsync, Vsync, video_on, 
    output logic[$clog2(H_VISIBLE)-1:0] video_x, 
    output logic[$clog2(V_VISIBLE)-1:0] video_y
);

    import vga_controller_pkg::*;

    localparam  H_VIDEO_ON = (H_SYNC + H_BACK), 
                H_VIDEO_OFF = (H_VIDEO_ON + H_VISIBLE);
    localparam  V_VIDEO_ON = (V_SYNC + V_BACK),
                V_VIDEO_OFF = (V_VIDEO_OFF + V_VISIBLE);

    logic[$clog2(H_TOTAL)-1:0] Hcount;
    logic[$clog2(V_TOTAL)-1:0] Vcount;

    always_comb begin
        if(video_on) begin
            video_x = (Hcount - (H_SYNC + H_BACK));
            video_y = (Vcount - (V_SYNC + V_BACK));
        end else
            video_x = '0;
            video_y = '0;
    end

    always_ff @(posedge clk or posedge areset) begin
        if(areset || (Hcount == (H_TOTAL-1)))
            Hcount <= 1'b0;
        else
            Hcount <= Hcount + 1;

        if(areset || (Vcount == (V_TOTAL-1)))
            Vcount <= 1'b0;
        else
            Vcount <= Vcount + 1;

    end

    assign Hsync = (Hcount >= H_SYNC);
    assign Vsync = (Vcount >= V_SYNC);
    assign video_on = ( ((Hcount >= H_VIDEO_ON) || (Hcount < H_VIDEO_OFF)) && 
                        ((Vcount >= V_VIDEO_ON) || (Vcount < V_VIDEO_OFF)) );

endmodule



/*

Module for managing Hsync, Vsync, and video_on timings

*/

import vga_controller_pkg::*;

module vga_timing(
    input logic clk, areset,
    output logic Hsync, Vsync, video_on, 
    output logic[$clog2(H_VISIBLE)-1:0] video_x, 
    output logic[$clog2(V_VISIBLE)-1:0] video_y
);

    localparam [$clog2(H_TOTAL)-1:0] H_VIDEO_ON = (H_SYNC + H_BACK);
    localparam [$clog2(H_TOTAL)-1:0] H_VIDEO_OFF = (H_VIDEO_ON + H_VISIBLE);
    localparam [$clog2(V_TOTAL)-1:0] V_VIDEO_ON = (V_SYNC + V_BACK);
    localparam [$clog2(V_TOTAL)-1:0] V_VIDEO_OFF = (V_VIDEO_ON + V_VISIBLE);

    logic[$clog2(H_TOTAL)-1:0] Hcount;
    logic[$clog2(V_TOTAL)-1:0] Vcount;

    always_comb begin
        video_x = '0;
        video_y = '0;
        
        if(video_on) begin
            video_x = Hcount - H_VIDEO_ON;
            video_y = 9'(Vcount - V_VIDEO_ON);
        end
    end

    always_ff @(posedge clk or posedge areset) begin
        if(areset) begin
            Vcount <= '0;
            Hcount <= '0;
        end else if(Hcount == (H_TOTAL-1)) begin
            Hcount <= '0;

            if(Vcount == (V_TOTAL-1))
                Vcount <= '0;
            else
                Vcount <= Vcount + 1;
        end else
            Hcount <= Hcount + 1;
    end

    assign Hsync = areset ? 1'b1 : (Hcount >= H_SYNC);
    assign Vsync = areset ? 1'b1 : (Vcount >= V_SYNC);
    assign video_on = ( ((Hcount >= H_VIDEO_ON) && (Hcount < H_VIDEO_OFF)) && 
                        ((Vcount >= V_VIDEO_ON) && (Vcount < V_VIDEO_OFF)) );

endmodule




import vga_controller_pkg::*;

module vga_controller_top(
    input logic clk, areset,
    output logic Hsync, Vsync,
    output logic [3:0] red, green, blue
);

    logic on;
    logic [$clog2(H_VISIBLE)-1:0] x;
    logic [$clog2(V_VISIBLE)-1:0] y;
    logic new_clk;

    clk_gen clk_gen(    .clk(clk), 
                        .new_clk(new_clk)
                        );

    vga_timing vga_timing(  .clk(new_clk), 
                            .areset(areset), 
                            .Hsync(Hsync), 
                            .Vsync(Vsync), 
                            .video_on(on),
                            .video_x(x), 
                            .video_y(y)
                            );

    pixel_renderer pixel_renderer(  .on(on), 
                                    .x(x), 
                                    .y(y), 
                                    .red(red), 
                                    .green(green), 
                                    .blue(blue)
                                    );

endmodule
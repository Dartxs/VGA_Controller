import vga_controller_pkg::*;

module vga_controller_top(
    input logic clk, areset, up, down, left, right,
    output logic Hsync, Vsync,
    output logic [3:0] red, green, blue
);

    logic on;
    logic [$clog2(H_VISIBLE)-1:0] x;
    logic [$clog2(V_VISIBLE)-1:0] y;
    logic [$clog2(SPRITE_MAX_X+1)-1:0] sprite_x;
    logic [$clog2(SPRITE_MAX_Y+1)-1:0] sprite_y;
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
                                    .sprite_x(sprite_x),
                                    .sprite_y(sprite_y),
                                    .x(x), 
                                    .y(y), 
                                    .red(red), 
                                    .green(green), 
                                    .blue(blue)
                                    );
                                    
    sprite_controller sprite_controller( .clk(clk), 
                                         .areset(areset), 
                                         .up(up), 
                                         .down(down), 
                                         .left(left), 
                                         .right(right),
                                         .sprite_x(sprite_x),
                                         .sprite_y(sprite_y)
                                    );  

endmodule
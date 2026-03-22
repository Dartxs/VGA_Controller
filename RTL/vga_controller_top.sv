import vga_controller_pkg::*;

module vga_controller_top(
    input logic clk, reset, up, down, left, right, next, prev,
    output logic Hsync, Vsync,
    output logic [3:0] red, green, blue
);

    logic on;
    logic [$clog2(H_VISIBLE)-1:0] x;
    logic [$clog2(V_VISIBLE)-1:0] y;
    logic [$clog2(CHAR_MAX_X+1)-1:0] sprite_x;
    logic [$clog2(CHAR_MAX_Y+1)-1:0] sprite_y;
    logic [$clog2(CHAR_TOTAL)-1:0] char_select
    logic new_clk, reset_tick, up_level, down_level, left_level, right_level, next_tick, prev_tick;
    
    button_debouncer reset_debouncer(.clk(clk), .btn(reset), .level(), .tick(reset_tick));
    button_debouncer up_debouncer(.clk(clk), .btn(up), .level(up_level), .tick());
    button_debouncer down_debouncer(.clk(clk), .btn(down), .level(down_level), .tick());
    button_debouncer left_debouncer(.clk(clk), .btn(left), .level(left_level), .tick());
    button_debouncer right_debouncer(.clk(clk), .btn(right), .level(right_level), .tick());
    button_debouncer next_debouncer(.clk(clk), .btn(next), .level(), .tick(next_tick));
    button_debouncer prev_debouncer(.clk(clk), .btn(prev), .level(), .tick(prev_tick));


    clk_gen clk_gen (   .clk(clk), 
                        .new_clk(new_clk)
                    );

    vga_timing vga_timing (  .clk(new_clk), 
                            .reset(reset_tick), 
                            .Hsync(Hsync), 
                            .Vsync(Vsync), 
                            .video_on(on),
                            .video_x(x), 
                            .video_y(y)
                            );

    pixel_renderer pixel_renderer ( .on(on), 
                                    .char_select(char_select),
                                    .sprite_x(sprite_x),
                                    .sprite_y(sprite_y),
                                    .x(x), 
                                    .y(y), 
                                    .red(red), 
                                    .green(green), 
                                    .blue(blue)
                                );
                                    
    sprite_controller sprite_controller ( .clk(clk),
                                         .reset(reset_tick), 
                                         .up(up_level), 
                                         .down(down_level), 
                                         .left(left_level), 
                                         .right(right_level),
                                         .sprite_x(sprite_x),
                                         .sprite_y(sprite_y)
                                        );  

    char_selector char_selector (   .clk(clk),
                                    .reset(reset_tick),
                                    .next_tick(next_tick),
                                    .prev_tick(prev_tick),
                                    .char_select(char_select)
                                );

endmodule
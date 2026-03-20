import vga_controller_pkg::*;

module sprite_controller#(
    parameter int MOVE_FREQ = 60
    )(
    input logic clk, areset, up, down, left, right,
    output logic [$clog2(SPRITE_MAX_X+1)-1:0] sprite_x,
    output logic [$clog2(SPRITE_MAX_Y+1)-1:0] sprite_y
);

    localparam int sprite_per = 100000000/MOVE_FREQ;
    localparam int tick_width = (sprite_per <= 1) ? 1 : $clog2(sprite_per);
    logic [tick_width-1:0] tick;


    logic [$clog2(SPRITE_MAX_X+1)-1:0] next_x;
    logic [$clog2(SPRITE_MAX_Y+1)-1:0] next_y;

    always_comb begin
        next_x = sprite_x;
        next_y = sprite_y;

        if(up && (sprite_y != '0))
            next_y = sprite_y - 1;
        else if(down && (sprite_y != SPRITE_MAX_Y))
            next_y = sprite_y + 1;

        if(left && (sprite_x != '0))
            next_x = sprite_x - 1;
        else if(right && (sprite_x != SPRITE_MAX_X))
            next_x = sprite_x + 1;
    end

    always_ff @(posedge clk or posedge areset) begin 
        if(areset) begin
            sprite_x <= '0;
            sprite_y <= '0;
            tick <= '0;
        end else if(tick == tick_width'(sprite_per-1))begin
            sprite_x <= next_x;
            sprite_y <= next_y;
            tick <= '0;
        end else
            tick <= tick + 1;
    end

endmodule





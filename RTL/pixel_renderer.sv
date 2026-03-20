/*

Module for setting color of pixels, x or y inputs may

*/

import vga_controller_pkg::*;

module pixel_renderer(
    input logic on,
    input logic [$clog2(SPRITE_MAX_X+1)-1:0] sprite_x,
    input logic [$clog2(SPRITE_MAX_Y+1)-1:0] sprite_y,
    input logic[$clog2(H_VISIBLE)-1:0] x, 
    input logic[$clog2(V_VISIBLE)-1:0] y,
    output logic [3:0] red, green, blue
);

    logic [SPRITE_X_DIM-1:0] rom [0:SPRITE_Y_DIM-1];

    localparam rom_width_x = $clog2(SPRITE_X_DIM);
    localparam rom_width_y = $clog2(SPRITE_Y_DIM);

    logic [rom_width_x-1:0] rom_x;
    logic [rom_width_y-1:0] rom_y;

    initial begin
        $readmemb("../../ROM/heart_rom_16x16.mem", rom);
    end

    always_comb begin
        {red, green, blue, rom_x, rom_y} = '0;

        if(on) begin
            {red, green, blue} = 12'hFFF;
            if((x >= sprite_x) && (y >= sprite_y) && ((sprite_x + SPRITE_X_DIM) > x) && ((sprite_y + SPRITE_Y_DIM) > y)) begin
                rom_x = rom_width_x'(x-sprite_x);
                rom_y = rom_width_y'(y-sprite_y);
                
                blue = (rom[rom_y][rom_x]) ? 4'h0 : 4'hF;
                green = (rom[rom_y][rom_x]) ? 4'h0 : 4'hF;
            end 
        end
    end

endmodule
/*

Module for setting color of pixels, x or y inputs may

*/

import vga_controller_pkg::*;

module pixel_renderer(
    input logic on,
    input logic[$clog2(H_VISIBLE)-1:0] x, 
    input logic[$clog2(V_VISIBLE)-1:0] y,
    output logic [3:0] red, green, blue
);

    logic [3:0] on_ratio; 

    always_comb begin
        {red, green, blue} = '0;

        on_ratio = (y < 240) ? 4'hF : 4'h8; //fully on in the upper half of screen, about half on in the lower half

        if(on) begin
            if(x < 213)
                red = on_ratio;
            else if(x < 426)
                green = on_ratio;
            else
                blue = on_ratio;
        end
    end

endmodule
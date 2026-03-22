package vga_controller_pkg;

    parameter H_SYNC = 96;
    parameter H_BACK = 48;
    parameter H_VISIBLE = 640;
    parameter H_FRONT = 16;
    parameter H_TOTAL = 800;
    

    parameter V_SYNC = 2;
    parameter V_BACK = 33;
    parameter V_VISIBLE = 480;
    parameter V_FRONT = 10;
    parameter V_TOTAL = 525;

    parameter CHAR_TOTAL = 256;
    parameter CHAR_X_DIM = 8;
    parameter CHAR_Y_DIM = 8;
    parameter CHAR_MAX_X = H_VISIBLE - CHAR_X_DIM;
    parameter CHAR_MAX_Y = V_VISIBLE - CHAR_Y_DIM;

    parameter SPRITE_X_DIM = 8;
    parameter SPRITE_Y_DIM = 8;
    parameter SPRITE_MAX_X = H_VISIBLE - SPRITE_X_DIM;
    parameter SPRITE_MAX_Y = V_VISIBLE - SPRITE_Y_DIM;

endpackage
    
## Architecture

The design is composed of the following modules:

- **vga_timing** — generates hsync, vsync, and the current pixel coordinates (x, y) from a 25MHz pixel clock
- **clk_gen** — simulation stub for the MMCM used in Vivado
- **pixel_renderer** — reads the font ROM and determines the color of each pixel based on sprite position and selected character
- **sprite_controller** — tracks sprite position and handles boundary-clamped movement from debounced button inputs
- **char_selector** — cycles through all 256 characters in the font ROM on button press
- **button_debouncer** — hardware debounces all button inputs
- **vga_controller_top** — top-level wrapper connecting all modules and mapping to FPGA I/O

### Display Parameters

| Parameter | Value |
|---|---|
| Resolution | 640 x 480 |
| Refresh Rate | 60 Hz |
| Color Depth | 12-bit (4-bit per channel) |
| Pixel Clock | 25 MHz |
| Sprite Size | 8 x 8 pixels |
| Character Set | 256 characters (8 x 8 font ROM) |

### Font ROM

The font ROM is a 256-entry x 8-row memory where each row is an 8-bit value representing one row of pixels for a character. A 1 in the ROM indicates a filled pixel, a 0 indicates background. The ROM is loaded from font_rom.mem at synthesis time using $readmemb.

The character set includes printable ASCII characters and custom glyphs to fill all 256 entries.

### Package

All timing constants and sprite/character dimensions are defined in `vga_controller_pkg.sv` and imported across all modules.

## Verification

All modules were verified using [cocotb](https://www.cocotb.org/) with Verilator as the simulator.

## Synthesis

Synthesized and implemented in Vivado targeting the **Nexys A7 (XC7A100T-CSG324)**.

| Metric | Value |
|---|---|
| System Clock | 100 MHz |
| Pixel Clock | 25 MHz (generated via MMCM) |
| LUTs | 451 (~0.71% of available) |
| Flip Flops | 217 (~0.17% of available) |
| MMCM | 1 |
| Timing | All constraints met (WNS = +2.546 ns) |
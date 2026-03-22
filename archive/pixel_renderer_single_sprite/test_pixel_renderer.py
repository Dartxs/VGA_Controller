import cocotb
from cocotb.triggers import Timer
import random

import timings

def check_color(dut, sprite_x, sprite_y, x, y, on):
    actual_red = dut.red.value.to_unsigned()
    actual_green = dut.green.value.to_unsigned()
    actual_blue = dut.blue.value.to_unsigned()

    red = 0
    green = 0
    blue = 0

    if(on):
        red = 0xF
        green = 0xF
        blue = 0xF
        if((x >= sprite_x) and 
           (y >= sprite_y) and 
           ((sprite_x + 16) > x) and 
           ((sprite_y + 16) > y)):
            
            rom = [
            [int(bit) for bit in line.strip()]
            for line in """
            0000000000000000
            0000110000110000
            0001111001111000
            0011111111111100
            0111111111111110
            0111111111111110
            1111111111111111
            1111111111111111
            0111111111111110
            0011111111111100
            0001111111111000
            0000111111110000
            0000011111100000
            0000001111000000
            0000000110000000
            0000000000000000
            """.strip().splitlines()
            ]

            blue = 0 if (rom[y-sprite_y][x-sprite_x] == 1) else 0xF
            green = 0 if (rom[y-sprite_y][x-sprite_x] == 1) else 0xF

    assert (actual_red == red), (
        f"\nOutput Color Mismatch\n"
        f"For on = {bool(on)} at ({x}, {y})\n"
        f"Expected red = {red:1X}, actual red = {actual_red:1x}"
    )

    assert (actual_green == green), (
        f"\nOutput Color Mismatch\n"
        f"For on = {bool(on)} at ({x}, {y})\n"
        f"Expected green = {green:1X}, actual green = {actual_green:1x}"
    )

    assert (actual_blue == blue), (
        f"\nOutput Color Mismatch\n"
        f"For on = {bool(on)} at ({x}, {y})\n"
        f"Expected blue = {blue:1X}, actual blue = {actual_blue:1x}"
    )


@cocotb.test()
async def test_pixel_renderer(dut):

    on = 0
    x = 0
    y = 0
    sprite_x = 0
    sprite_y = 0

    dut.on.value = on
    dut.x.value = x
    dut.y.value = y
    dut.sprite_x.value = sprite_x
    dut.sprite_y.value = sprite_y

    await Timer(1, 'ns')

    on = 1
    for i in range (100000):
        x = random.randint(0, timings.H_VISIBLE-1)
        y = random.randint(0, timings.V_VISIBLE-1)
        sprite_x = random.randint(0, timings.SPRITE_MAX_X)
        sprite_y = random.randint(0, timings.SPRITE_MAX_Y)

        dut.on.value = on
        dut.x.value = x
        dut.y.value = y
        dut.sprite_x.value = sprite_x
        dut.sprite_y.value = sprite_y
        await Timer(1, 'ns')

        check_color(dut, sprite_x, sprite_y, x, y, on)   



    
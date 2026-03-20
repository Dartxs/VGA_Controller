import cocotb
from cocotb.triggers import Timer
import random

import timings

def check_color(dut, x, y, on):
    actual_red = dut.red.value.to_unsigned()
    actual_green = dut.green.value.to_unsigned()
    actual_blue = dut.blue.value.to_unsigned()

    red = 0
    green = 0
    blue = 0

    if(on):
        actual_on_ratio = dut.on_ratio.value.to_unsigned()
        on_ratio = 0xF if (y < 240) else 0x8
        assert (actual_on_ratio == on_ratio), (
            f"\nOn_ratio Mismatch\n"
            f"For ({x}, {y})\n"
            f"Expected on_ratio = {actual_on_ratio}, actual = {on_ratio}\n"
        )

        red_on = True if (x < 213) else False
        green_on = True if ((x >= 213) and (x < 426)) else False
        blue_on = True if (x >= 426) else False

        red = on_ratio if (red_on) else 0
        blue = on_ratio if(blue_on) else 0
        green = on_ratio if(green_on) else 0

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

    dut.on.value = on
    dut.x.value = x
    dut.y.value = y

    await Timer(1, 'ns')
    check_color(dut, x, y, on)

    on = 1
    for i in range (500):
        x = random.randint(0, timings.H_VISIBLE)
        y = random.randint(0, timings.V_VISIBLE)

        dut.on.value = on
        dut.x.value = x
        dut.y.value = y
        await Timer(1, 'ns')

        check_color(dut, x, y, on)    



    
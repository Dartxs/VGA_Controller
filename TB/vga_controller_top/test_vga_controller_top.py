import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

import timings

def start_clock(dut, period=10):
    clock = Clock(dut.clk, period, 'ns')
    cocotb.start_soon(clock.start())

async def init_test(dut):
    start_clock(dut)

    dut.areset.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, 'ns')
    check_outputs(dut, 0)
    dut.areset.value = 0

def check_rgb(dut, x, y, on):
    actual_red = dut.red.value.to_unsigned()
    actual_green = dut.green.value.to_unsigned()
    actual_blue = dut.blue.value.to_unsigned()

    red = 0
    green = 0
    blue = 0

    if(on):
        on_ratio = 0xF if (y < 240) else 0x8

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


def check_syncs(dut, Hcount, Vcount, areset):
    H_SYNC = timings.H_SYNC
    Hsync = int(dut.Hsync.value)
    expected_Hsync = int((Hcount >= H_SYNC) or areset)
    assert (Hsync == expected_Hsync), (
        f"OUTPUT MISMATCH"
        f"For Hcount = {Hcount} and Vcount = {Vcount}\n"
        f"expected Hsync = {expected_Hsync}, actual Hsync = {Hsync}\n"
    )

    V_SYNC = timings.V_SYNC
    Vsync = int(dut.Vsync.value)
    expected_Vsync = int((Vcount >= V_SYNC) or areset) 
    assert (Vsync == expected_Vsync), (
        f"OUTPUT MISMATCH\n"
        f"For Hcount = {Hcount} and Vcount = {Vcount}\n"
        f"expected Vsync = {expected_Vsync}, actual Vsync = {Vsync}\n"
    )

def check_outputs(dut, clkCycles):
    areset = (clkCycles == 0)
    H_TOTAL = timings.H_TOTAL
    Hcount = int(clkCycles % H_TOTAL)
    Vcount = clkCycles // H_TOTAL

    H_video_on = timings.H_SYNC + timings.H_BACK
    H_video_off = H_video_on + timings.H_VISIBLE
    V_video_on = timings.V_SYNC + timings.V_BACK
    V_video_off = V_video_on + timings.V_VISIBLE

    video_on = ((Hcount >= H_video_on) and (Hcount < H_video_off) and
                (Vcount >= V_video_on) and (Vcount < V_video_off) and (not areset))
    
    x = (Hcount - H_video_on) if (video_on) else 0
    y = (Vcount - V_video_on) if (video_on) else 0

    check_rgb(dut, x, y, video_on)
    check_syncs(dut, Hcount, Vcount, areset)

@cocotb.test()
async def test_vga_controller_top(dut):
    await init_test(dut)

    for i in range (1, 420000):
        await RisingEdge(dut.clk)
        await Timer(1, 'ns')
        check_outputs(dut, i)

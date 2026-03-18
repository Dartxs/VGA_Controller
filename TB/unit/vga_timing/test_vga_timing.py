import cocotb
from cocotb.triggers import Timer, ClockCycles, RisingEdge
from cocotb.clock import Clock
import random

import timings

def start_clock(dut, period=10):
    clock = Clock(dut.clk, period, 'ns')
    cocotb.start_soon(clock.start())

async def init_test(dut):
    start_clock(dut)

    dut.areset.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, 'ns')
    dut.areset.value = 0

def check_inital(dut):
    Hsync = int(dut.Hsync.value)
    Vsync = int(dut.Vsync.value)
    video_x = int(dut.video_x.value)
    video_y = int(dut.video_y.value)

    assert(Hsync == 1), (
        f"FAILED RESET TEST\n"
        f"expected Hsync = 0 | actual Hsync = {Hsync}\n"
    )
    assert(Vsync == 1), (
        f"FAILED RESET TEST\n"
        f"expected Vsync = 0 | actual Vsync = {Vsync}\n"
    )
    assert(video_x == 0), (
        f"FAILED RESET TEST\n"
        f"expected video_x = 0 | actual video_x = {video_x}\n"
    )
    assert(video_y == 0), (
        f"FAILED RESET TEST\n"
        f"expected video_y = 0 | actual video_y = {video_y}\n"
    )

def check_syncs(dut, Hcount, Vcount):
    H_SYNC = timings.H_SYNC
    Hsync = int(dut.Hsync.value)
    expected_Hsync = int(Hcount >= H_SYNC)
    assert (Hsync == expected_Hsync), (
        f"OUTPUT MISMATCH"
        f"For Hcount = {Hcount} and Vcount = {Vcount}\n"
        f"expected Hsync = {expected_Hsync}, actual Hsync = {Hsync}\n"
    )

    V_SYNC = timings.V_SYNC
    Vsync = dut.Vsync.value
    expected_Vsync = int(Vcount >= V_SYNC)
    assert (Vsync == expected_Vsync), (
        f"OUTPUT MISMATCH\n"
        f"For Hcount = {Hcount} and Vcount = {Vcount}\n"
        f"expected Vsync = {expected_Vsync}, actual Vsync = {Vsync}\n"
    )

def check_video(dut, Hcount, Vcount):
    H_video_on = timings.H_SYNC + timings.H_BACK
    H_video_off = H_video_on + timings.H_VISIBLE
    V_video_on = timings.V_SYNC + timings.V_BACK
    V_video_off = V_video_on + timings.V_VISIBLE

    video_on = int((Hcount >= H_video_on) and (Hcount < H_video_off) and
                         (Vcount >= V_video_on) and (Vcount < V_video_off))
    actual_video_on = int(dut.video_on.value)
    assert (actual_video_on == video_on), (
        f"OUTPUT MISMATCH\n"
        f"For Hcount = {Hcount} and Vcount = {Vcount}\n"
        f"expected video_on = {video_on}, actual video_on = {actual_video_on}\n"
    )    

    video_x = (Hcount - H_video_on) if (actual_video_on) else 0
    actual_video_x = int(dut.video_x.value)
    assert (actual_video_x == video_x), (
        f"OUTPUT MISMATCH\n"
        f"For Hcount = {Hcount} and Vcount = {Vcount}\n"
        f"expected video_x = {video_x}, actual video_x = {actual_video_x}\n"
    )

    video_y = (Vcount - V_video_on) if (actual_video_on) else 0
    actual_video_y = int(dut.video_y.value)
    assert (actual_video_y == video_y), (
        f"OUTPUT MISMATCH\n"
        f"For Hcount = {Hcount} and Vcount = {Vcount}\n"
        f"expected video_y = {video_y}, actual video_y = {actual_video_y}\n"
    )

def check_outputs(dut, clkCycles):
    clkCycles %= 420000
    H_TOTAL = timings.H_TOTAL
    expected_Hcount = int(clkCycles % H_TOTAL)
    actual_Hcount = int(dut.Hcount.value)
    assert (actual_Hcount == expected_Hcount), (
        f"OUTPUT MISMATCH\n"
        f"clkCycles = {clkCycles}\n"
        f"expected Hcount = {expected_Hcount}, actual Hcount = {actual_Hcount}\n"
    )

    expected_Vcount = clkCycles // H_TOTAL
    actual_Vcount = int(dut.Vcount.value)
    assert (actual_Vcount == expected_Vcount), (
        f"Count MISMATCH\n"
        f"clkCycles = {clkCycles}\n"
        f"expected Vcount = {expected_Vcount}, actual Vcount = {actual_Vcount}\n"
    )

    check_syncs(dut, expected_Hcount, expected_Vcount)
    check_video(dut, expected_Hcount, expected_Vcount)


@cocotb.test()
async def test_vga_timing(dut):

    await init_test(dut)
    check_inital(dut)
    tot_cycles = 0

    for i in range (25):
        cycles = random.randint(1, 419999)
        tot_cycles += cycles
        await ClockCycles(dut.clk, cycles)
        await Timer(1, 'ns')

        check_outputs(dut, tot_cycles)





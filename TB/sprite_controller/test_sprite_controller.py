import cocotb
from cocotb.triggers import RisingEdge, Timer, ClockCycles
from cocotb.clock import Clock

import timings

def start_clock(dut):
    clock = Clock(dut.clk, 10, 'ns')
    cocotb.start_soon(clock.start())

async def check_pos(dut, x, y):

    await Timer(1, 'ns')
    actual_x = dut.sprite_x.value.to_unsigned()
    assert (actual_x == x), (
        f"\nPosition Mismatch\n"
        f"Expected x = {actual_x}, actual x = {x}\n"
    )

    actual_y = dut.sprite_y.value.to_unsigned()
    assert (actual_y == y), (
        f"\nPosition Mismatch\n"
        f"Expected y = {actual_y}, actual y = {y}\n"
    )

async def init_test(dut):
    start_clock(dut)
    dut.areset.value = 1
    await check_pos(dut, 0, 0)
    dut.areset.value = 0
    
@cocotb.test()
async def test_sprite_controller(dut):
    await init_test(dut)

    x = 0
    y = 0

    #test idle position
    await ClockCycles(dut.clk, 50)
    await check_pos(dut, x, y)

    #test going left at (0,0)
    dut.left.value = 1
    await RisingEdge(dut.clk)
    await check_pos(dut, x, y)
    dut.left.value = 0

    #test going up at (0,0)
    dut.up.value = 1
    await RisingEdge(dut.clk)
    await check_pos(dut, x, y)
    dut.up.value = 0

    #Move to far right
    dut.right.value = 1
    await ClockCycles(dut.clk, timings.SPRITE_MAX_X)
    x = timings.SPRITE_MAX_X
    await check_pos(dut, x, y)

    #Test going right at right border
    await RisingEdge(dut.clk)
    await check_pos(dut, x, y)
    dut.right.value = 0

    #Move all the way down
    dut.down.value = 1
    await ClockCycles(dut.clk, timings.SPRITE_MAX_Y)
    y = timings.SPRITE_MAX_Y
    await check_pos(dut, x, y)

    #Test going down at bottom
    await RisingEdge(dut.clk)
    await check_pos(dut, x, y)
    
    #Test all switches pressed
    dut.up.value = 1
    dut.right.value = 1
    dut.left.value = 1
    x -= 1
    y -= 1
    await RisingEdge(dut.clk)
    await check_pos(dut, x, y)

    #Test going down-right
    dut.up.value = 0
    dut.left.value = 0
    x += 1
    y += 1
    await RisingEdge(dut.clk)
    await check_pos(dut, x, y)

    #Test reset
    dut.areset.value = 1
    x = 0
    y = 0
    await check_pos(dut, x, y)



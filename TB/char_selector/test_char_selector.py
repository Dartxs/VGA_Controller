import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

def start_clock(dut):
    clock = Clock(dut.clk, 10, 'ns')
    cocotb.start_soon(clock.start())

async def check_char_select(dut, char_select):

    await Timer(1, 'ns')
    actual_char_select= dut.char_select.value.to_unsigned()
    assert (actual_char_select == char_select), (
        f"\n Mismatch Output\n"
        f"Expected char_select = {char_select}, actual char_select = {actual_char_select}\n"
    )

async def init_test(dut):
    start_clock(dut)
    dut.reset.value = 1
    await check_char_select(dut, 0)
    dut.reset.value = 0

@cocotb.test()
async def test_char_selector(dut):
    await init_test(dut)

    #test previous at 0
    dut.prev_tick.value = 1
    await RisingEdge(dut.clk)
    await check_char_select(dut, 255)
    dut.prev_tick.value = 0

    #tests going next at 255 and continues to check to ensure output increments correctly
    dut.next_tick.value = 1
    for i in range (256):
        await RisingEdge(dut.clk)
        await check_char_select(dut, i)

    #test reset
    dut.reset.value = 1
    await check_char_select(dut, 0)


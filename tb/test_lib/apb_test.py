# test_apb.py
import cocotb
from cocotb.clock import Clock
from top.apb_bus import apb_bus
from env.apb_env import apb_env
from seq_lib.apb_generator import apb_generator
MEMSIZE=64
async def setup(dut, period=10):
    bus = apb_bus(dut)                  
    cocotb.start_soon(Clock(bus.PCLK, period, unit="ns").start())
    env = apb_env(bus)
    await env.start()
    return env

@cocotb.test()
async def apb_write_read(dut):
    env = await setup(dut)
    await env.sequence.write(0x00, 0xDEADBEEF)
    data, err = await env.sequence.read(0x00)
    assert data == 0xDEADBEEF
    assert err == 0
    await env.finish()

@cocotb.test()
async def apb_reset_test(dut):
    env= await setup(dut)
    for i in range(MEMSIZE):
        await env.sequence.write(i*4, 0xA5A5A5A5 ^ i)
    
    await env.agent.driver.reset()
    
    for i in range(MEMSIZE):
        data, err= await env.sequence.read(i*4)
        assert data==0, f"addr {i*4} did not clear after reset"
        assert err==0

@cocotb.test()
async def apb_overwrite(dut):
    env = await setup(dut)
    await env.sequence.write(0x00, 0xDEADBEEF)
    await env.sequence.write(0x00, 0x12345678)
    await env.sequence.write(0x00, 0x77777777)
    data, err = await env.sequence.read(0x00)
    await env.finish()

@cocotb.test()
async def apb_seq_rd_wr(dut):
    env = await setup(dut)
    for i in range(MEMSIZE):
        await env.sequence.write(i*4, 0xDEADBEEF)
    for i in range(MEMSIZE):
        data, err = await env.sequence.read(i*4)
    await env.finish()

@cocotb.test()
async def apb_con_rd_wr(dut):
    env = await setup(dut)
    for i in range(MEMSIZE):
        await env.sequence.write(i*4, 0xDEADBEEF)
        data, err = await env.sequence.read(i*4)
    await env.finish()
@cocotb.test()
async def apb_random(dut):
    env = await setup(dut)
    await env.generator.run(n=50)
    await env.finish()   

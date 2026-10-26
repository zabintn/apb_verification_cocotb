# apb_env.py
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from agent.apb_agent import apb_agent
from env.apb_scoreboard import apb_scoreboard
from top.apb_transaction import apb_txn
from generator.apb_generator import apb_generator
MEMSIZE=64
class apb_env:
    def __init__(self, bus):
        self.bus = bus
        self.agent = apb_agent(bus)
        self.scoreboard = apb_scoreboard(self.agent.monitor.ap)
        self.generator = apb_generator(self.agent.driver.req_q, mem_bytes=MEMSIZE * 4)

    async def start(self, period_ns=10):
        cocotb.start_soon(Clock(self.bus.PCLK, period_ns, unit="ns").start())
        await self.agent.driver.reset()     
        await self.agent.start()
        cocotb.start_soon(self.scoreboard.run())

    async def write(self, addr, data):
        txn = apb_txn(write=True, addr=addr, wdata=data)
        await self.agent.driver.req_q.put(txn)
        await txn.done.wait()
        return txn

    async def read(self, addr):
        txn = apb_txn(write=False, addr=addr)
        await self.agent.driver.req_q.put(txn)
        await txn.done.wait()
        return txn.rdata, txn.slverr

    async def finish(self):
        for _ in range(5):                   
            await RisingEdge(self.bus.PCLK)
        self.scoreboard.report()

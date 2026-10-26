# apb_env.py
import cocotb
from cocotb.triggers import RisingEdge
from agent.apb_agent import apb_agent
from cocotb.queue import Queue
from env.apb_scoreboard import apb_scoreboard
from top.apb_transaction import apb_txn
from seq_lib.apb_generator import apb_generator
from seq_lib.apb_sequence import apb_sequence
MEMSIZE=64
class apb_env:
    def __init__(self, bus):
        self.bus = bus
        self.req_q = Queue()
        self.agent = apb_agent(bus, req_q=self.req_q)
        self.sequence= apb_sequence(self.req_q)
        self.scoreboard = apb_scoreboard(self.agent.monitor.ap)
        self.generator = apb_generator(self.agent.driver.req_q, mem_bytes=MEMSIZE * 4)
    async def start(self):
        await self.agent.driver.reset()     
        await self.agent.start()
        cocotb.start_soon(self.scoreboard.run())

    async def finish(self):
        for _ in range(5):                   
            await RisingEdge(self.bus.PCLK)
        self.scoreboard.report()

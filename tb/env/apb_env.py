# apb_env.py
import cocotb
from cocotb.triggers import RisingEdge
from agent.apb_agent import apb_agent
from cocotb.queue import Queue
from env.apb_scoreboard import apb_scoreboard
from top.apb_transaction import apb_txn
from seq_lib.apb_generator import apb_generator
from seq_lib.apb_sequence import apb_sequence
from env.apb_coverage import apb_coverage
from cocotb_coverage.coverage import coverage_db
MEMSIZE=64
class apb_env:
    def __init__(self, bus):
        self.bus = bus
        self.req_q = Queue()
        self.agent = apb_agent(bus, req_q=self.req_q)
        self.sequence= apb_sequence(self.req_q)
        self.scoreboard = apb_scoreboard(self.agent.monitor.ap)
        self.generator = apb_generator(self.agent.driver.req_q, mem_bytes=MEMSIZE * 4)
        self.coverage = apb_coverage(self.agent.monitor.cov_q)
    async def start(self):
        await self.agent.driver.reset()     
        await self.agent.start()
        cocotb.start_soon(self.scoreboard.run())
        cocotb.start_soon(self.coverage.run())

    async def finish(self):
        for _ in range(5):                   
            await RisingEdge(self.bus.PCLK)

        coverage_db.report_coverage(print, bins=True)
        print(f"Total: {coverage_db['apb'].cover_percentage:.1f}%")
        for name in ["apb.addr", "apb.err", "apb.op", "apb.wr_err"]:
            print(f"{name}: {coverage_db[name].cover_percentage:.1f}%")
        self.scoreboard.report()

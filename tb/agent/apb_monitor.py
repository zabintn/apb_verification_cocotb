import logging
from cocotb.queue import Queue
from cocotb.triggers import RisingEdge
from top.apb_transaction import apb_txn
class apb_monitor:
    def __init__(self, bus):
        self.bus = bus
        self.ap = Queue()
        self.cov_q= Queue()
        self.log=logging.getLogger("cocotb.apb_monitor")
    async def run(self):
        while True:
            await RisingEdge(self.bus.PCLK)

            if self.bus.PSEL.value & self.bus.PENABLE.value & self.bus.PREADY.value:
                txn = self.sample()
                self.log.info(f"observed: {txn}")
                await self.ap.put(txn)
                await self.cov_q.put(txn)
    def sample(self):
        bus = self.bus
        txn = apb_txn()
        txn.write = int(bus.PWRITE.value)
        txn.addr =  int(bus.PADDR.value)
        if txn.write:
            txn.wdata = int(bus.PWDATA.value)
        else:
            txn.rdata = int(bus.PRDATA.value)
        txn.pslverr = int(bus.PSLVERR.value)
        return txn

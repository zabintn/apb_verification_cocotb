from cocotb.queue import Queue
from cocotb.triggers import RisingEdge
class apb_driver:
    def __init__(self, bus):
        self.bus = bus
        self.req_q = Queue()

    async def reset(self):
        self.bus.PRESETn.value=0
        self.bus.PSEL.value=0
        self.bus.PWRITE.value=0
        self.bus.PENABLE.value=0
        self.bus.PADDR.value=0
        self.bus.PWDATA.value=0

        for _ in range(5):
            await RisingEdge(self.bus.PCLK)
        self.bus.PRESETn.value = 1
        await RisingEdge(self.bus.PCLK)
        
    async def run(self):
        while True:
            txn=await self.req_q.get()
            await self.drive(txn)
            txn.done.set()
    async def drive(self, txn):
        bus = self.bus

        await RisingEdge(bus.PCLK)
        bus.PSEL.value=1
        bus.PENABLE.value=0
        bus.PWRITE.value=int(txn.write)
        bus.PADDR.value=txn.addr
        bus.PWDATA.value=txn.wdata if txn.write else 0

        await RisingEdge(bus.PCLK)
        bus.PENABLE.value=1

        await RisingEdge(bus.PCLK)
        while not bus.PREADY.value:
            await RisingEdge(bus.PCLK)

        if not txn.write:
            txn.rdata = int(bus.PRDATA.value)
        txn.slverr=int(bus.PSLVERR.value)

        bus.PSEL.value=0
        bus.PENABLE.value=0

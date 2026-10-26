from cocotb_coverage.coverage import CoverPoint, CoverCross, coverage_db

class apb_coverage:
    def __init__(self, mon_q):
        self.mon_q=mon_q

    async def run(self):
        while True:
            txn = await self.mon_q.get()
            self.sample(txn)

    @CoverPoint("apb.op", xf=lambda self, txn: "WR" if txn.write else "RD",
                bins=["WR", "RD"])
    
    @CoverPoint("apb.addr", xf=lambda self, txn:txn.addr, 
                bins=[(0, 255), (256, 0xFFFFFFFF)],
                rel=lambda val, b: b[0] <= val <= b[1],
                bins_labels=["valid", "invalid"])

    @CoverPoint("apb.err", xf=lambda self, txn: txn.pslverr,
                bins=[0,1])

    @CoverCross("apb.wr_err", items=["apb.op", "apb.err"])

    def sample(self, txn):
        pass



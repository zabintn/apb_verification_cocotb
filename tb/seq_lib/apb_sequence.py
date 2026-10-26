from top.apb_transaction import apb_txn
class apb_sequence:

    def __init__(self, req_q):
        self.req_q =  req_q

    async def write(self, addr, data):
        txn= apb_txn(write=True, addr=addr, wdata=data)
        await self.req_q.put(txn)
        await txn.done.wait()
        return txn

    async def read(self, addr):
        txn= apb_txn(write=False, addr=addr)
        await self.req_q.put(txn)
        await txn.done.wait()
        return txn.rdata, txn.pslverr

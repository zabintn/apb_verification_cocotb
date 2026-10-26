import random
from top.apb_transaction import apb_txn

class apb_generator:
    def __init__(self, out_q, mem_bytes=256):
        self.out_q = out_q  
        self.mem_bytes = mem_bytes

    def rand_addr(self):
        limit = self.mem_bytes
        return random.randrange(0, limit, 4)

    def rand_txn(self, write_ratio=0.5):
        write = random.random() < write_ratio
        return apb_txn(write=write,
                       addr=self.rand_addr(),
                       wdata=random.getrandbits(32) if write else 0)

    async def run(self, n=100, write_ratio=0.5, valid=True):
        txn = None
        for _ in range(n):
            txn = self.rand_txn(write_ratio)
            await self.out_q.put(txn)
        if txn:
            await txn.done.wait()   

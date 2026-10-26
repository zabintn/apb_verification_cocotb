import random

class apb_generator:
    def __init__(self, env, mem_bytes=256):
        self.env = env
        self.mem_bytes = mem_bytes

    def rand_addr(self):
        limit = self.mem_bytes
        return random.randrange(0, limit, 4) #start, stop, step size

    async def random_traffic(self, n=100, write_ratio=0.5, valid=True):
        for _ in range(n):
            addr = self.rand_addr()
            if random.random() < write_ratio:
                await self.env.write(addr, random.getrandbits(32))
            else:
                await self.env.read(addr)

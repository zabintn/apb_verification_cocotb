class apb_scoreboard:
    def __init__(self, mon_q):
        self.mon_q = mon_q
        self.last_addr = {}          # addr -> last written data
        self.errors = 0
        self.checked = 0

    async def run(self):
        while True:
            txn = await self.mon_q.get()
            self.check(txn)

    def check(self, txn):
        if txn.write:
            self.last_addr[txn.addr] = txn.wdata
        elif txn.addr in self.last_addr:
            self.checked += 1
            expected = self.last_addr[txn.addr]
            if txn.rdata != expected:
                self.errors += 1
                print(f"MISMATCH addr=0x{txn.addr:X} "
                      f"expected=0x{expected:X} got=0x{txn.rdata:X}")

    def report(self):
        print(f"Scoreboard: {self.checked} reads checked, {self.errors} errors")
        assert self.errors == 0, f"{self.errors} scoreboard mismatches"

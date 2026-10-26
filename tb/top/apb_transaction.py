from dataclasses import dataclass, field
from cocotb.triggers import Event
@dataclass
class apb_txn:
    write: int = 1
    addr: int = 0
    wdata: int = 0 
    rdata: int = 0
    slverr: int = 0
    done: Event = field(default_factory=Event, repr=False, compare=False)
def __str__(self):
     return f"{'WR' if self.write else 'RD'} addr=0x{self.addr:X} wdata=0x{self.wdata:X} rdata=0x{self.rdata:X}"

import cocotb
from agent.apb_driver import apb_driver
from agent.apb_monitor import apb_monitor

class apb_agent:
    def __init__(self, bus, active=True):
        self.driver = apb_driver(bus) if active else None
        self.monitor = apb_monitor(bus)

    async def start(self):
        if self.driver:
            cocotb.start_soon(self.driver.run())
        cocotb.start_soon(self.monitor.run())

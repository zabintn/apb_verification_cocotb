from top.apb_config import DEFAULT_MAP
class apb_bus:
    def __init__(self, dut, signal_map=None):
        m = {**DEFAULT_MAP, **(signal_map or {})}    # user overrides win
        for std_name, dut_name in m.items():
            setattr(self, std_name, getattr(dut, dut_name))

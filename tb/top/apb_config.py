APB_SIGNALS = ["PCLK", "PRESETn", "PSEL", "PENABLE", "PWRITE",
               "PADDR", "PWDATA", "PRDATA", "PREADY", "PSLVERR"]

DEFAULT_MAP = {name: name for name in APB_SIGNALS}   # identity mapping

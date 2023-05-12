import micropython as mpy
import gc

import epd4in2b as epd

mpy.mem_info()

gc.enable()
gc.collect()

# 可分配的内存大小有限制
# GC: total: 124032, used: 7456, free: 116576
# MemoryError: memory allocation failed, allocating 15000 bytes

epd.EPD_HEIGHT = 300 if gc.mem_free() >= (15000*8) else 200
epd.epd_test()

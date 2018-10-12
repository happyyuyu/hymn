from hymn import Simulator
import numpy as np

mem = np.array([0]*32, dtype=np.int8)
mem[0] = 33
mem[1] = -118
mem[2] = -65
mem[3] = -98
mem[4] = -65
mem[10] = 36
a = Simulator(mem)
a.run(1)

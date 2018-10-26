from hymn import Simulator, Parser
import numpy as np

#TODO: create a unittest suite for testing
# mem = np.array([0]*32, dtype=np.int8)
# mem[0] = 33
# mem[1] = -118
# mem[2] = -65
# mem[3] = -98
# mem[4] = -65
# mem[10] = 36
# a = Simulator(mem)
# a.run(1)

p = Parser("./simulator/testsuites/test3.txt")
print(p.get_mem()) 
print(p.get_labels())
print(p.get_pending())

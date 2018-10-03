from hymn import Simulator


mem = [0]*32
mem[0] = 33
mem[1] = -118
mem[2] = -65
mem[10] = 36
a = Simulator(mem)
a.run(1)

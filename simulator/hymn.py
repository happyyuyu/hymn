"""
An implementation of the SimHymn simulator.

Includes a parser and interpreter for the SimHYMN instructions.

Author: Harry Zhou
"""
from collections import deque

class Simulator:
    def __init__(self):
        memory = []
        for i in range(32):
            memory[i] = [0,0]
        self._memory=memory
        self._pc = 0
        self._ir = 0
        self._ac = 0
        self._input = 0
        self._output = 0
        self._zero_flag = True
        self._positive_flag = False

    def __init__(self, mem, pc, ir, ac):
        self._memory = mem
        self._pc = pc
        self._ir = ir 
        self._ac = ac
        self._input = 0
        self._output = 0
        self._zero_flag = True
        self._positive_flag = False

    def _exec_jump(self, addr):
        self._pc = addr 

    def _exec_jzer(self, addr):
        if self._zero_flag:
            self._pc = addr     

    def _exec_jpos(self, addr):
        if self._positive_flag:
            self._pc = addr 

    def _exec_load(self, addr):
        self._memory[addr][1] = self._ac

    def _exec_stor(self, addr):
        self._memory = self._ac 

    def _exec_sub(self, addr):
        self._ac -= self._memory[addr][1]

    def _exec_add(self, addr):
        self._ac += self._memory[addr][1]


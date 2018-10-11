"""
An implementation of the SimHymn simulator.

Includes a parser and interpreter for the SimHYMN instructions.

Author: Harry Zhou
"""
from collections import deque
import numpy as np

class Simulator:
    def __init__(self, mem):
        self._memory = np.array(mem).astype(np.int8)
        self._pc = 0
        self._ir = 0
        self._ac = 0
        self._io = ""
        self._done = False
        self._zero_flag = True
        self._positive_flag = False
        self.INSTRUCTIONS = {1: self._exec_jump,
                             2: self._exec_jzer,  
                             3: self._exec_jpos,
                             4: self._exec_load,
                             5: self._exec_stor,
                             6: self._exec_add,
                             7: self._exec_sub}

    def run(self, verbose=0):
        while not self._done and self._pc < 30:
            self.step(verbose)
        print("io: ", self._io)
        return self._io

    def step(self, verbose, jump=False):
        self._ir = self._memory[self._pc]
        instrn = np.right_shift(self._memory[self._pc], 5) & 7
        num = np.int8(self._memory[self._pc] - (instrn << 5))
        print("num: ", np.binary_repr(instrn, width=8))
        if instrn == 0:
            self._done = True
            return
        self.INSTRUCTIONS[instrn](num)     
        if verbose == 1:
            print("pc: ", self._pc)
            print("ir: ", self._ir)
            print("ac: ", self._ac)
        if (jump==False):
            self._pc += 1

    def _exec_jump(self, addr):
        self._pc = addr 
        self.step(1, True)

    def _exec_jzer(self, addr):
        if self._zero_flag:
            self._pc = addr     

    def _exec_jpos(self, addr):
        if self._positive_flag:
            self._pc = addr 

    def _exec_load(self, addr):
        if addr==30:
            self._io += "? "
            user_input = input("? ")
            self._io += user_input
            self._memory[addr] = np.int8(user_input)
        self._ac = self._memory[addr]

    def _exec_stor(self, addr):
        if addr==31:
            self._io += str(self._ac)
        self._memory[addr] = self._ac 

    def _exec_sub(self, addr):
        self._ac -= self._memory[addr]

    def _exec_add(self, addr):
        self._ac += self._memory[addr]

    def out(self):
        print(self._io)
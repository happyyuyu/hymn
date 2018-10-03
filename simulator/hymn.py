"""
An implementation of the SimHymn simulator.

Includes a parser and interpreter for the SimHYMN instructions.

Author: Harry Zhou
"""
from collections import deque

class Simulator:

    def __init__(self, mem=[0]*32):
        self._memory = mem
        self._pc = 0
        self._ir = 0 
        self._ac = 0
        self._io = ""
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
        done = False
        while not done and self._pc < 30:
            self._ir = self._memory[self._pc]
            bits = self._to_unsigned_bin8(self._memory[self._pc])
            instrn = bits >> 5
            num = bits - (instrn << 5)
            if verbose == 1:
                print("pc: ", self._pc)
                print("ir: ", self._ir)
                print("ac: ", self._ac)
            if instrn == 0:
                done = True
                break
            self.INSTRUCTIONS[instrn](num)
            self._pc += 1
        print(self._io)
        return self._io

    def _exec_jump(self, addr):
        self._pc = addr 

    def _exec_jzer(self, addr):
        if self._zero_flag:
            self._pc = addr     

    def _exec_jpos(self, addr):
        if self._positive_flag:
            self._pc = addr 

    def _exec_load(self, addr):
        if addr==31:
            self._io += "? "
            user_input = input("? ")
            self._io += user_input
            self._memory[addr] = user_input
        self._ac = self._memory[addr]

    def _exec_stor(self, addr):
        if addr==32:
            self._io += self._ac
        self._memory[addr] = self._ac 

    def _exec_sub(self, addr):
        self._ac -= self._memory[addr]

    def _exec_add(self, addr):
        self._ac += self._memory[addr]

    def _to_unsigned_bin8(self, num):
        if num < 0:
            return (1 << 8) - (0 - num) 
        return num

    def out(self):
        print(self._io)
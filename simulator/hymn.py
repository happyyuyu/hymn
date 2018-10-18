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
        self._verbose = 0
        self.INSTRUCTIONS = {1: self._exec_jump,
                             2: self._exec_jzer,  
                             3: self._exec_jpos,
                             4: self._exec_load,
                             5: self._exec_stor,
                             6: self._exec_add,
                             7: self._exec_sub}

    def run(self, verbose=0):
        self._verbose = verbose
        while not self._done and self._pc < 30:
            self.step()
        print("io: ", self._io)
        return self._io

    def step(self, jump=False):
        self._ir = self._memory[self._pc]
        instrn = np.right_shift(self._memory[self._pc], 5) & 7
        num = np.int8(self._memory[self._pc] - (instrn << 5))
        # print("num: ", np.binary_repr(instrn, width=8))
        if instrn == 0:
            self._done = True
            return     
        if self._verbose == 1:
            print("pc: ", self._pc)
            print("ir: ", self._ir)
            print("ac: ", self._ac)
            print("zf: ", self._zero_flag)
            print("pf: ", self._positive_flag)
            print()
        self.INSTRUCTIONS[instrn](num)
        if (jump==False):
            self._pc += 1

    def _exec_jump(self, addr):
        self._pc = addr 
        self.step(True)

    def _exec_jzer(self, addr):
        if self._zero_flag:
            self._pc = addr     
            self.step(True)

    def _exec_jpos(self, addr):
        if self._positive_flag:
            self._pc = addr 
            self.step(True)

    def _exec_load(self, addr):
        if addr==30:
            self._io += "? "
            user_input = input("? ")
            self._io += user_input + "\n"
            self._memory[addr] = np.int8(user_input)
        self._ac = self._memory[addr]
        self._set_flags()

    def _exec_stor(self, addr):
        if addr==31:
            self._io += str(self._ac)
            self._io += "\n"
        self._memory[addr] = self._ac 

    def _exec_sub(self, addr):
        self._ac -= self._memory[addr]
        self._set_flags()

    def _exec_add(self, addr):
        self._ac += self._memory[addr]
        self._set_flags()

    def _set_flags(self):
        if self._ac == 0:
            self._zero_flag = True
            self._positive_flag = False
        elif self._ac > 0:
            self._zero_flag = False
            self._positive_flag = True
        else:
            self._zero_flag = False
            self._positive_flag = False
        
    def out(self):
        print(self._io)


class Parser:
    def __init__(self, filename):
        with open(filename, 'r') as in_file:
            lines = in_file.readlines()

        lines = [line.strip() for line in lines]  # clean up
        lines = [line._remove_comment() for line in lines] # remove comment

        self._mem = np.array([0]*32, dtype=np.int8)
        labels = dict()

        self._mem_ids = [0 for i in range(len(lines))]
        self._currrent_id = 0

        # Get all the labels
        for index, line in enumerate(lines):
            if ":" in line:
                labels[":"] = index
        self._errors = ""

    def _remove_comment(self, line):
        if "#" in line:
            pos = line.find("#")
            line = line[:pos]
        return line
    
    def _find_label(self, index, lines):
        self._mem_ids[index] = -1
        if lines[index].endswith(":"):
            if index = len(lines) - 1:
                #TODO: May have problem if the last lines are empty
                self._errors += "Line "+str(index+1)+": Lable Precedes end of file" 
            else:
                segments = line.split(":")
                self._check_label_segs(segments)

        else:
            self._mem_ids[index] = self._currrent_id
            self._currrent_id += 1
            segments = line.split(":")
            last_seg = segments.pop()
            self._check_label_segs(segments)  

    def _check_label_segs(self, segments):
            for seg in segments:
                if " " in seg.strip():
                    self._errors += "Line "+str(index+1)+": Lables cannot contain white space"
                else:
                    labels[seg] = index

    
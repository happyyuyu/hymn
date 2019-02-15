"""
An implementation of the SimHymn simulator.

Includes a parser and interpreter for the SimHYMN instructions.

Author: Yuhan (Harry) Zhou
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
        lines = [self._remove_comment(line) for line in lines] # remove comment

        self._mem = np.array([0]*32, dtype=np.int8)
        self._aux_lines = []
        self._labels = dict()
        self._pending_labels = []
        self._currrent_id = 0
        self._instrn_table = {"jump": 1,
                             "jzer": 2,
                             "jpos": 3,
                             "load": 4,
                             "stor": 5,
                             "add": 6,
                             "sub": 7,
                             "store": 5}

        # Get all the labels
        self._errors = ""
        for index, line in enumerate(lines):
            self._process_line(index, lines)
        
        if self._pending_labels:
            for label, line_num in self._pending_labels:
                self._errors += "Line " + str(line_num+1)+": Lable precedes end of file\n"

        for cur_index, line_info in enumerate(self._aux_lines):
            self._parse_instrn(line_info[0],cur_index,line_info[1])
        
        # print(self._aux_lines)

    def _remove_comment(self, line):
        if "#" in line:
            pos = line.find("#")
            line = line[:pos]
        return line
    
    def _process_line(self, index, lines):
        if lines[index].endswith(":"):
            # if index == len(lines) - 1:
            #     #TODO: May have problem if the last lines are empty
            #     self._errors += "ahhh"#"Line "+str(index+1)+": Lable precedes end of file" 
            # else:
            #     segments = lines[index].split(":")
            #     self._check_label_segs(segments, index, pending=True)
            segments = lines[index].split(":")
            self._check_label_segs(segments, index, pending=True)

        else:
            if lines[index].isspace() or lines[index] == '':
                return
            segments = lines[index].split(":")
            last_seg = segments.pop()
            self._aux_lines.append((last_seg, index))
            self._check_label_segs(segments, index)  

    def _check_label_segs(self, segments, index, pending=False):
        for seg in segments:
            seg = seg.strip()
            if " " in seg.strip().split():
                self._errors += "Line "+str(index+1)+": Labels cannot contain white space"
            elif seg.isspace() or seg == '':
                pass 
            else:
                if pending:
                    self._pending_labels.append((seg, index))
                else:
                    for label, line_num in self._pending_labels:
                        print(label,self._aux_lines)
                        self._labels[label] = len(self._aux_lines) - 1
                    del self._pending_labels[:]
                    self._labels[seg] = len(self._aux_lines) - 1

    def _check_binary(self, string):
        # TODO: Figure out under what circumstances should it be binary. 
        if len(string) != 8:
            return False
        for char in string:
            if char != "0" and char != "1":
                return False
        return True

    def _parse_instrn(self, string, cur_index, index):
        segs = string.split()
        # need to take care of empty strings
        if len(segs) == 1:
            if segs[0].lower() == "write":
                self._mem[cur_index] = -65
            elif segs[0].lower() == "halt":
                self._mem[cur_index] = 0
            elif segs[0].lower() == "read":
                self._mem[cur_index] = -98  
            elif self._check_binary(segs[0]):
                self._mem[cur_index] = np.int8(int(segs[0],2)) 
            elif segs[0].isdigit():
                self._mem[cur_index] = np.int8(segs[0])
            elif segs[0][0]=='-' and segs[0][1:].isdigit():
                self._mem[cur_index] = np.int8(segs[0])
            elif segs[0] in self._labels:
                self._mem[cur_index] = np.int8(self._labels[segs[0]])
            else:
                print(segs[0], string)
                self._errors += "Error"
        elif len(segs) == 2:
            segs[0] = segs[0].lower()
            if segs[0] in self._instrn_table:
                instrn = np.int8(self._instrn_table[segs[0]])
                if self._check_binary(segs[1]):
                    self._mem[cur_index] = (instrn << 5) + np.int8(int(segs[1],2)) 
                elif segs[1].isdigit():
                    num = np.int8(segs[1])
                    self._mem[cur_index] = (instrn << 5) + num
                elif segs[1][0]=='-' and segs[1][1:].isdigit():
                    self._mem[cur_index] = (instrn << 5) + np.int8(segs[1])
                elif segs[1] in self._labels:
                    num = np.int8(self._labels[segs[1]])              
                    self._mem[cur_index] = (instrn << 5) + num
            # pass          

    def get_mem(self):
        if not self._errors:
            return self._mem
        else:
            return self._errors

    def get_labels(self):
        return self._labels

    def get_pending(self):
        return self._pending_labels
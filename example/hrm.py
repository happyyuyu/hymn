"""
An implementation of the Human Resource Machine architecture.

Includes a parser and interpreter for the HRM language.

Author: Raghuram Ramanujan
"""
from collections import deque


class MachineSession:
    def __init__(self, program, memory, inputs):
        self._pc = 0  # program counter
        self._program = program
        self._memory = memory
        self._holding = None
        self._inputs = deque(inputs)
        self._outputs = deque()
        self._input_exhausted = False
        self.JUMP_TABLE = {'noop':     self._exec_noop,
                           'inbox':    self._exec_inbox,
                           'outbox':   self._exec_outbox,
                           'copyfrom': self._exec_copy_from,
                           'copyto':   self._exec_copy_to,
                           'add':      self._exec_add,
                           'sub':      self._exec_sub,
                           'jump':     self._exec_jump,
                           'jumpz':    self._exec_jumpz,
                           'jumpn':    self._exec_jumpn,
                           'bumpup':   self._exec_bumpup,
                           'bumpdn':   self._exec_bumpdn}

    def run(self):
        done = False
        while not done and not self._input_exhausted:
            instrn = self._program[self._pc]
            opcode = instrn[0]
            arg = instrn[1] if len(instrn) == 2 else None
            self._pc += 1
            if not self._program.is_label(opcode):
                self.JUMP_TABLE[opcode](arg)
            if self._pc >= len(self._program):
                done = True
        return tuple(self._outputs)

    def _exec_noop(self, _):
        pass

    def _exec_inbox(self, _):
        try:
            self._holding = self._inputs.popleft()
        except IndexError:
            self._holding = None
            self._input_exhausted = True

    def _exec_outbox(self, _):
        self._outputs.append(self._holding)
        self._holding = None

    def _exec_copy_from(self, addr):
        self._holding = self._memory[addr]

    def _exec_copy_to(self, addr):
        self._memory[addr] = self._holding

    def _exec_add(self, addr):
        self._holding += self._memory[addr]

    def _exec_sub(self, addr):
        self._holding -= self._memory[addr]

    def _exec_jump(self, addr):
        self._pc = addr

    def _exec_jumpz(self, addr):
        if self._holding == 0:
            self._pc = addr

    def _exec_jumpn(self, addr):
        if self._holding < 0:
            self._pc = addr

    def _exec_bumpup(self, addr):
        self._memory[addr] += 1
        self._holding = self._memory[addr]

    def _exec_bumpdn(self, addr):
        self._memory[addr] -= 1
        self._holding = self._memory[addr]


class Program:
    def __init__(self, filename):
        with open(filename, 'r') as in_file:
            lines = in_file.readlines()

        lines = [line for line in lines if not line.startswith('--')]  # remove header
        lines = [line.strip().lower() for line in lines]  # clean up
        lines = [line for line in lines if len(line) > 0]  # remove empty lines
        lines = [line for line in lines if not line.startswith('comment')]  # remove comments

        # remove comment/label definitions if any
        idx = self._find_first_def(lines)
        lines = lines[:idx] if idx != -1 else lines

        # only lines left now should either be labels or instructions
        self._instructions = list()
        labels = dict()
        for idx, line in enumerate(lines):
            # a label, associate with a pointer to the next instruction
            if self.is_label(line):
                labels[line[:-1]] = self._find_next_instruction(lines, idx+1)
            # tokenize line and add to list of instructions
            tokens = line.split()
            self._instructions.append(tokens)

        # translate all label arguments into addresses and cast to ints
        for instrn in self._instructions:
            if len(instrn) == 2:
                if instrn[1] in labels:
                    instrn[1] = labels[instrn[1]]
                instrn[1] = int(instrn[1])

        # append no-op in case program ends with label(s), to avoid out-of-bounds
        # errors
        if any(v == len(self._instructions) for v in labels.values()):
            self._instructions.append(['noop'])

    def _find_first_def(self, lines):
        for idx, str_ in enumerate(lines):
            if str_.startswith('define'):
                return idx
        return -1  # not found

    def _find_next_instruction(self, lines, start_index):
        i = start_index
        while i < len(lines) and lines[i].endswith(':'):
            i += 1
        return i

    def is_label(self, instruction):
        return instruction.endswith(':')

    def get_num_instructions(self):
        count = 0
        for i in self._instructions:
            if not self.is_label(i[0]):
                count += 1
        return count

    def __getitem__(self, idx):
        return self._instructions[idx]

    def __len__(self):
        return len(self._instructions)

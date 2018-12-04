import sys
import os
sys.path.append('./..')
from hymn import Simulator, Parser
import numpy as np
import pytest


def parse_program(filename):
    try:
        prog = Parser(filename)
    except IOError:
        print("Cannot read file: ", filename)
        return
    return prog

def generate_mem(values,positions):
    mem = np.array([0]*32, dtype=np.int8)
    for i in range(len(values)):
        mem[positions[i]] = values[i]
    return mem

def test_text_1():
    p = parse_program("./test1.txt")
    mem = generate_mem([-124,-28,-65,5,5,-98], [0,1,2,4,5,6])
    np.testing.assert_array_equal(p.get_mem(), mem)

def test_text_2():
    p = parse_program("./test2.txt")
    mem = generate_mem([-65,-98], [0,2])
    np.testing.assert_array_equal(p.get_mem(), mem)

def test_text_3():
    p = parse_program("./test3.txt")
    mem = generate_mem([-124,-28,-65,5,5,-98], [0,1,2,4,5,6])
    np.testing.assert_array_equal(p.get_mem(), mem)

def read_answer(filename):
    try:
        with open(filename, 'r') as in_file:
            lines = in_file.readlines()
    except:
        print("Cannot read file: ", filename)
        return
    mems = np.array([0]*32, dtype=np.int8)
    for line_num, line in enumerate(lines):
        hex_num = "0x" + line.strip()
        int_num = int(hex_num, 16)
        # print(int_num)
        # np.append(mems,[np.int8(int_num)])
        mems[line_num] = int_num
    return mems

def comp_student_case(filenumber):
    filename = "../hymn_student_cases/" + str(filenumber) + ".txt"
    mems = read_answer(filenumber)
    p = parse_program(filename)
    p_mem = p.get_mem()
    assert all(i==j for i,j in zip(p_mem, mems))
    
@pytest.mark.skip
def test_student_cases(dir="./student/student_case_results"):
    directory = os.fsencode(dir)

    for filenum in os.listdir(directory):
        fnum = filenum.decode('UTF-8')
        fnum_path = "./student/student_case_results/" +fnum
        filename = "./student/hymn_student_cases/" + str(fnum) + ".txt"
        print(fnum_path, filename)
        mems = read_answer(fnum_path)
        p = parse_program(filename)
        p_mem = p.get_mem()
        np.testing.assert_array_equal(p_mem, mems)

@pytest.mark.parametrize('filenum', [x for x in os.listdir(os.fsencode("./student/student_case_results"))])
def test_single_case(filenum):
    fnum = filenum.decode('UTF-8')
    fnum_path = "./student/student_case_results/" +fnum
    filename = "./student/hymn_student_cases/" + str(fnum) + ".txt"
    print(fnum_path, filename)
    mems = read_answer(fnum_path)
    p = parse_program(filename)
    p_mem = p.get_mem()
    np.testing.assert_array_equal(p_mem, mems)
""""
Unit tests for HW 1, CSC 121.

Author: Raghuram Ramanujan
"""
import unittest
from gradescope_utils.autograder_utils.decorators import weight, visibility
from timeout_decorator import timeout
import hrm


class TestHumanResourceMachine(unittest.TestCase):
    def _parse_program(self, filename):
        try:
            prog = hrm.Program(filename)
        except IOError:
            self.fail('Could not find file {}. Double-check that the file you '
                      'uploaded is correctly named and is in plain text '
                      'format.'.format(filename))
        return prog

    @timeout(1)
    @weight(2)
    def test_0_scrambler_handler(self):
        """ Testing solution to the Scrambler Handler. """
        prog = self._parse_program('scrambler_handler.txt')
        session = hrm.MachineSession(program=prog,
                                     memory=[0, 0, 0],
                                     inputs=(4, 9, 65, 69, 1, 7))
        results = session.run()
        expected = (9, 4, 69, 65, 7, 1)
        self.assertEqual(results, expected,
                         'Submitted solution does not compute the correct '
                         'results on all inputs.')

    @timeout(1)
    @weight(1.5)
    def test_1_tetracontiplier_solution_length(self):
        """ Testing if solution to the Tetracontiplier is of the correct length. """
        prog = self._parse_program('tetracontiplier.txt')
        self.assertLessEqual(prog.get_num_instructions(), 14,
                             'Submitted solution is longer than 14 instructions.')

    @timeout(1)
    @weight(2.5)
    def test_2_tetracontiplier(self):
        """ Testing solution to the Tetracontiplier. """
        prog = self._parse_program('tetracontiplier.txt')
        session = hrm.MachineSession(program=prog,
                                     memory=[None, None, None, None, None],
                                     inputs=(7, -4, 4, 0))
        results = session.run()
        expected = (280, -160, 160, 0)
        self.assertEqual(results, expected,
                         'Submitted solution does not compute the correct '
                         'results on all inputs.')

    @timeout(1)
    @weight(4)
    def test_3_equalization_room(self):
        """ Testing solution to the Equalization Room. """
        prog = self._parse_program('equalization_room.txt')
        session = hrm.MachineSession(program=prog,
                                     memory=[None, None, None],
                                     inputs=(3, 6, 2, 2, -1, 9, -6, -6))
        results = session.run()
        expected = (2, -6)
        self.assertEqual(results, expected,
                         'Submitted solution does not compute the correct '
                         'results on all inputs.')

    @timeout(1)
    @weight(4)
    def test_4_exclusive_lounge(self):
        """ Testing solution to the Exclusive Lounge. """
        prog = self._parse_program('exclusive_lounge.txt')
        session = hrm.MachineSession(program=prog,
                                     memory=[None, None, None, None, 0, 1],
                                     inputs=(9, -3, -3, -7, 7, -8, 4, 8))
        results = session.run()
        expected = (1, 0, 1, 0)
        self.assertEqual(results, expected,
                         'Submitted solution does not compute the correct '
                         'results on all inputs.')

    @timeout(1)
    @weight(5)
    def test_5_countdown(self):
        """ Testing solution to the Countdown. """
        prog = self._parse_program('countdown.txt')
        session = hrm.MachineSession(program=prog,
                                     memory=[None] * 10,
                                     inputs=(3, -4, 0, 3))
        results = session.run()
        expected = (3, 2, 1, 0, -4, -3, -2, -1, 0, 0, 3, 2, 1, 0)
        self.assertEqual(results, expected,
                         'Submitted solution does not compute the correct '
                         'results on all inputs.')

    @timeout(1)
    @weight(6)
    def test_6_multiplication_workshop(self):
        """ Testing solution to the Multiplication Workshop. """
        prog = self._parse_program('multiplication_workshop.txt')
        session = hrm.MachineSession(program=prog,
                                     memory=[None] * 9 + [0],
                                     inputs=(7, 4, 5, 4, 8, 0, 0, 9, 1, 6))
        results = session.run()
        expected = (28, 20, 0, 0, 6)
        self.assertEqual(results, expected,
                         'Submitted solution does not compute the correct '
                         'results on all inputs.')

    # ----------------- Extra credit test cases -----------------
    @timeout(1)
    @weight(1)
    @visibility('hidden')
    def test_7_cumulative_countdown(self):
        """ Testing solution to the Cumulative Countdown. """
        prog = self._parse_program('cumulative_countdown.txt')
        session = hrm.MachineSession(program=prog,
                                     memory=[None, None, None, None, None, 0],
                                     inputs=(3, 8, 0, 9))
        results = session.run()
        expected = (6, 36, 0, 45)
        self.assertEqual(results, expected,
                         'Submitted solution does not compute the correct '
                         'results on all inputs.')

    @timeout(1)
    @weight(1)
    @visibility('hidden')
    def test_8_three_sort(self):
        """ Testing solution to the Three Sort. """
        prog = self._parse_program('three_sort.txt')
        session = hrm.MachineSession(program=prog,
                                     memory=[None] * 10,
                                     inputs=(8, 5, 1, 2, 5, 8, 4, 7, 4, 5, -3, 0))
        results = session.run()
        expected = (1, 5, 8, 2, 5, 8, 4, 4, 7, -3, 0, 5)
        self.assertEqual(results, expected,
                         'Submitted solution does not compute the correct '
                         'results on all inputs.')
    # ----------------- Extra credit test cases -----------------

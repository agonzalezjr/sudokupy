import unittest


class SudokuBoard:
    def __init__(self, initial_state=None):
        if initial_state is None:
            self.__initial_state = "................................................................................."
        else:
            self.__initial_state = initial_state

    def initial_state(self):
        return self.__initial_state

    def pretty_initial_state(self):
        pass

    def print_nice(self):
        """ Prints the SudokuPuzzle to STDOUT in a nice table format """
        print "+---" * 9 + "+"
        for i in range(0, 9):
            print "|", " | ".join([str(c) for c in self.__initial_state[i]]), "|"
            print "+---" * 9 + "+"


class SudokuBoardTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        self.assertEqual(SudokuBoard().initial_state(),
                         ".................................................................................")

    def test_pretty(self):
        pass

    def tearDown(self):
        pass

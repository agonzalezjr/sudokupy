import unittest


class SudokuBoard:
    EMPTY_BOARD = "................................................................................."

    def __init__(self, initial_state=None):
        self.__state = self.EMPTY_BOARD
        if initial_state is None:
            self.__initial_state = self.EMPTY_BOARD
        else:
            self.__initial_state = initial_state

    @property
    def initial_state(self):
        return self.__initial_state

    @property
    def state(self):
        return self.__state

    def pretty_initial_state(self):
        return self.__pretty_helper(self.initial_state)

    def pretty(self):
        return self.__pretty_helper(self.state)

    def __pretty_helper(self, state):
        ret = ""
        for c in range(0, 9):
            if c > 0 and c % 3 == 0:
                ret += "------+-------+------\n"
            for r in range(0, 9):
                if r > 0 and r % 3 == 0:
                    ret += "| "
                ret += state[c * 9 + r] + " "
            ret += "\n"

        return ret


class SudokuBoardTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        self.assertEqual(SudokuBoard().initial_state, SudokuBoard.EMPTY_BOARD)

    def test_pretty(self):
        b1 = SudokuBoard()
        self.assertEqual(b1.pretty(), "")

    def tearDown(self):
        pass

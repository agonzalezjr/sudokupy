from SudokuCell import SudokuCell
import unittest


class SudokuBoard:
    EMPTY_BOARD = "................................................................................."
    DIGITS = '123456789'
    ROWS = 'ABCDEFGHI'
    COLUMNS = DIGITS

    def __init__(self, initial_state=None):
        self.__state = self.EMPTY_BOARD
        if initial_state is None:
            self.__initial_state = self.EMPTY_BOARD
        else:
            self.__initial_state = initial_state

        # create the cells
        self.__cells = []
        for r in self.ROWS:
            for c in self.COLUMNS:
                self.__cells.append(SudokuCell(r + c))


    @property
    def initial_state(self):
        return self.__initial_state

    @property
    def state(self):
        return self.__state

    @property
    def cells(self):
        return self.__cells

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
        self.assertEqual(len(SudokuBoard().initial_state), 81)
        self.assertEqual(SudokuBoard().initial_state, SudokuBoard.EMPTY_BOARD)

    def test_cells(self):
        self.assertEqual(len(SudokuBoard().cells), 81)

    def tearDown(self):
        pass

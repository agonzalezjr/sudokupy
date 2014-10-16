from SudokuCell import SudokuCell
import unittest


class SudokuBoard:
    EMPTY_BOARD = "................................................................................."
    DIGITS = '123456789'
    ROWS = 'ABCDEFGHI'
    COLUMNS = DIGITS

    def __init__(self, initial_state=None):
        if initial_state is None:
            self.__initial_state = self.EMPTY_BOARD
        else:
            self.__initial_state = initial_state

        # create the cells
        self.__squares = []
        self.__squaresHash = {}
        for r in self.ROWS:
            for c in self.COLUMNS:
                cell_name = r + c
                cell = SudokuCell(cell_name)
                self.__squares.append(cell)
                self.__squaresHash[cell_name] = cell

        # TODO: Merge these loops!

        # create the units
        # first the rows
        unitlist = []
        for c in self.COLUMNS:
            thisunit = []
            for r in self.ROWS:
                cell_name = r + c
                thisunit.append(self.squares_hash[cell_name])
            unitlist.append(thisunit)

        # then the columns
        for r in self.ROWS:
            thisunit = []
            for c in self.COLUMNS:
                cell_name = r + c
                thisunit.append(self.squares_hash[cell_name])
            unitlist.append(thisunit)

        # then the big sqares
        for rs in ['ABC', 'DEF', 'GHI']:
            for cs in ['123', '456', '789']:
                thisunit = []
                for r in rs:
                    for c in cs:
                        cell_name = r + c
                        thisunit.append(self.squares_hash[cell_name])
                unitlist.append(thisunit)

        # TODO: Move the units and peers to the cell objects

        # Create the units for each cell
        self.__units = {}
        for cell in self.squares:
            self.__units[cell] = []
            for unit in unitlist:
                if cell in unit:
                    self.__units[cell].append(unit)

        # Create the peers for each cell
        self.__peers = {}
        for cell in self.squares:
            self.__peers[cell] = set(sum(self.units[cell], [])) - set([cell])

        # Assign the initial values to each cell
        for i in range(0, len(self.initial_state)):
            if self.initial_state[i] in self.DIGITS:
                self.squares[i].assign(self.initial_state[i])



    @property
    def initial_state(self):
        return self.__initial_state

    @property
    def state(self):
        # Tge old way
        # ret = ""
        # for c in self.squares:
        #     ret += c.values if c.is_solved() else '.'
        # return ret

        # The Python way
        return ''.join(cell.values if cell.is_solved() else '.' for cell in self.squares)

    @property
    def squares(self):
        return self.__squares

    @property
    def squares_hash(self):
        return self.__squaresHash

    @property
    def units(self):
        return self.__units

    @property
    def peers(self):
        return self.__peers

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

    def pretty_values(self):
        ret = ""
        # The length of the widest cell
        width = max(len(cell.values) for cell in self.squares) + 1

        # The separator (some cool string operations with literals)
        line = "\n" + '+'.join(['-' * (width * 3)] * 3)

        for r in self.ROWS:
            ret += ''.join(self.squares_hash[r + c].values.center(width) + ('|' if c in '36' else '')
                           for c in self.COLUMNS)
            if r in 'CF':
                ret += line
            ret += "\n"

        return ret


# TODO: Revert the expected and actual values

class SudokuBoardTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        self.assertEqual(len(SudokuBoard().initial_state), 81)
        self.assertEqual(SudokuBoard().initial_state, SudokuBoard.EMPTY_BOARD)

    def test_cells(self):
        b = SudokuBoard()
        self.assertEqual(len(b.squares), 81)
        self.assertEqual(b.squares[0].name, 'A1')
        self.assertEqual(b.squares[23].name, 'C6')
        self.assertEqual(b.squares[80].name, 'I9')
        self.assertEqual(b.squares_hash['B5'].name, 'B5')

    def test_units(self):
        b = SudokuBoard()
        self.assertTrue(all(len(b.units[s]) == 3 for s in b.squares))
        self.assertEqual(b.units[b.squares_hash['C2']][0][0], b.squares_hash['A2'])
        self.assertEqual(b.units[b.squares_hash['C2']][1][2], b.squares_hash['C3'])
        self.assertEqual(b.units[b.squares_hash['C2']][2][8], b.squares_hash['C3'])

    def test_peers(self):
        b = SudokuBoard()
        self.assertTrue(all(len(b.peers[s]) == 20 for s in b.squares))
        self.assertTrue(all(b.squares_hash[cn] in b.peers[b.squares_hash['C2']])
                        for cn in ['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                                   'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                                   'A1', 'A3', 'B1', 'B3'])

    def tearDown(self):
        pass

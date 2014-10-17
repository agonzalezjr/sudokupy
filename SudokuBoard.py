from SudokuCell import SudokuCell
import unittest


class SudokuBoard:
    DIGITS = '123456789'
    ROWS = 'ABCDEFGHI'
    COLUMNS = DIGITS
    EMPTY_BOARD = '.' * len(ROWS) * len(COLUMNS)

    def __init__(self, initial_state=None):
        if initial_state is None:
            self.__initial_state = self.EMPTY_BOARD
        else:
            self.__initial_state = initial_state

        # create the cells
        self.__cells = []
        self.__cellsHash = {}
        for r in self.ROWS:
            for c in self.COLUMNS:
                cell_name = r + c
                cell = SudokuCell(cell_name, self)
                self.__cells.append(cell)
                self.__cellsHash[cell_name] = cell

        # create the units of the board
        unit_list = self.__get_unit_list()

        # let each cell know of the units it belongs to
        # (from this they will figure out all their peers)
        for cell in self.cells:
            for unit in unit_list:
                if cell in unit:
                    cell.add_unit(unit)

    @property
    def initial_state(self):
        return self.__initial_state

    @property
    def state(self):
        # Tge old way
        # ret = ""
        # for c in self.squares:
        # ret += c.values if c.is_solved() else '.'
        # return ret

        # The Python way
        return ''.join(cell.values if cell.is_solved() else '.' for cell in self.cells)

    @property
    def cells(self):
        return self.__cells

    @property
    def cells_hash(self):
        return self.__cellsHash

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
        width = max(len(cell.values) for cell in self.cells) + 1

        # The separator (some cool string operations with literals)
        line = "\n" + '+'.join(['-' * (width * 3)] * 3)

        for r in self.ROWS:
            ret += ''.join(self.cells_hash[r + c].values.center(width) + ('|' if c in '36' else '')
                           for c in self.COLUMNS)
            if r in 'CF':
                ret += line
            ret += "\n"

        return ret

    def __get_unit_list(self):
        unit_list = []

        # Each row is a unit
        for c in self.COLUMNS:
            thisunit = []
            for r in self.ROWS:
                cell_name = r + c
                thisunit.append(self.cells_hash[cell_name])
            unit_list.append(thisunit)

        # then the columns
        for r in self.ROWS:
            thisunit = []
            for c in self.COLUMNS:
                cell_name = r + c
                thisunit.append(self.cells_hash[cell_name])
            unit_list.append(thisunit)

        # then the big sqares
        for rs in ['ABC', 'DEF', 'GHI']:
            for cs in ['123', '456', '789']:
                thisunit = []
                for r in rs:
                    for c in cs:
                        cell_name = r + c
                        thisunit.append(self.cells_hash[cell_name])
                unit_list.append(thisunit)

        return unit_list

    def is_solved(self):
        return all(cell.is_solved() for cell in self.cells)

    def solve(self, debug_mode):
        # TODO: in case we need to re-iterate
        # iter = 0
        # while(not self.is_solved()):

        for i, d in enumerate(self.initial_state):
            if d in self.DIGITS:
                self.cells[i].assign(d)
                if debug_mode:
                    print(self.pretty_values())

# TODO: Revert the expected and actual values


class SudokuBoardTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        self.assertEqual(len(SudokuBoard().initial_state), 81)
        self.assertEqual(SudokuBoard().initial_state, SudokuBoard.EMPTY_BOARD)
        self.assertFalse(SudokuBoard().is_solved())

    def test_cells(self):
        b = SudokuBoard()
        self.assertEqual(len(b.cells), 81)
        self.assertEqual(b.cells[0].name, 'A1')
        self.assertEqual(b.cells[23].name, 'C6')
        self.assertEqual(b.cells[80].name, 'I9')
        self.assertEqual(b.cells_hash['B5'].name, 'B5')

    def test_units(self):
        b = SudokuBoard()
        self.assertTrue(all(len(c.units) == 3 for c in b.cells))
        c2 = b.cells_hash['C2']
        self.assertEqual(c2.units[0][0], b.cells_hash['A2'])
        self.assertEqual(c2.units[1][2], b.cells_hash['C3'])
        self.assertEqual(c2.units[2][8], b.cells_hash['C3'])

    def test_peers(self):
        b = SudokuBoard()
        self.assertTrue(all(len(c.peers) == 20 and c not in c.peers for c in b.cells))

    def test_solve(self):
        b = SudokuBoard()
        self.assertFalse(b.is_solved())

    def tearDown(self):
        pass

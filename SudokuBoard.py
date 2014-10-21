from SudokuCell import SudokuCell
import unittest


class SudokuBoard:
    """
    A Sudoku board
    """

    DIGITS = '123456789'
    ROWS = 'ABCDEFGHI'
    COLUMNS = DIGITS
    EMPTY_BOARD = '.' * len(ROWS) * len(COLUMNS)

    def __init__(self, initial_state=None):
        """
        Create a SudokuBoard
        :param initial_state: a string with the initial state of the puzzle.
        A '.' represents and empty cell. A character in DIGITS represents a solved
        cell.
        :return: SudokuBoard
        """

        if initial_state is None:
            self.__initial_state = self.EMPTY_BOARD
        else:
            self.__initial_state = initial_state

        assert len(self.initial_state) == len(self.ROWS) * len(self.COLUMNS)

        # create the cells
        self.__cells = []
        for r in self.ROWS:
            for c in self.COLUMNS:
                cell_name = r + c
                cell = SudokuCell(cell_name)
                self.__cells.append(cell)

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
        return ''.join(cell.values if cell.is_solved() else '.' for cell in self.cells)

    @property
    def cells(self):
        return self.__cells

    def cell_by_name(self, name):
        assert (len(name) == 2)
        assert (name[0] in self.ROWS)
        assert (name[1] in self.COLUMNS)
        return self.__cells[self.ROWS.index(name[0])*9 + self.COLUMNS.index(name[1])]

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
            ret += ''.join(self.cell_by_name(r + c).values.center(width) + ('|' if c in '36' else '')
                           for c in self.COLUMNS)
            if r in 'CF':
                ret += line
            ret += "\n"

        return ret

    def __get_unit_list(self):
        """
        :return: An array of all the units in the board. These are
        the groups of 9 cells that must contain unique values (all
        rows, all columns, and all 3x3 groupings, so there is 27 of
        these)
        """
        unit_list = []

        # Each row is a unit
        for c in self.COLUMNS:
            thisunit = []
            for r in self.ROWS:
                cell_name = r + c
                thisunit.append(self.cell_by_name(cell_name))
            unit_list.append(thisunit)

        # then the columns
        for r in self.ROWS:
            thisunit = []
            for c in self.COLUMNS:
                cell_name = r + c
                thisunit.append(self.cell_by_name(cell_name))
            unit_list.append(thisunit)

        # then the big sqares
        for rs in ['ABC', 'DEF', 'GHI']:
            for cs in ['123', '456', '789']:
                thisunit = []
                for r in rs:
                    for c in cs:
                        cell_name = r + c
                        thisunit.append(self.cell_by_name(cell_name))
                unit_list.append(thisunit)

        return unit_list
    def is_solved(self):
        """ Return True if the puzzle is solved """
        return all(cell.is_solved() for cell in self.cells)

    def solve(self, debug_mode=False):
        """
        Actually solve the puzzle using the information in the initial_state.
        It will first assign constraints and if needed search after that.
        :param debug_mode: Pass True to see progress and possibilities after each round
        :return: False if the puzzle is impossible
        """

        if self.is_solved():
            return True

        # Propagate constraints for the cell with the current state of the board
        for i, value in enumerate(self.initial_state):
            if value in self.DIGITS:
                if debug_mode:
                    print "Will ASSIGN ", value, " to cell ", self.cells[i].name, "... These are the current values:"
                    print self.pretty_values()
                if not self.cells[i].assign(value):
                    # We hit a contradiction assigning this value to a cell,
                    # Either it was a bad guess or the puzzle is malformed
                    return False
                if self.is_solved():
                    # It's solved with the constraints we have applied so far
                    return True

        # The board is still not solved, we'll search for a solution ...
        # Chose a solved cell with the fewest possibilities ...
        minimum, easiest = min((len(cell.values), cell) for cell in self.cells if not cell.is_solved())
        # ... and create a new puzzle out of using this guess ...
        for guess in easiest.values:
            guess_state_l = list(self.state)
            guess_state_l[self.ROWS.index(easiest.name[0])*9 + self.COLUMNS.index(easiest.name[1])] = guess
            new_board = SudokuBoard(''.join(guess_state_l))
            if new_board.solve(debug_mode):
                # ... if it solves the puzzle, steal the cells from the new board.
                self.__cells = new_board.cells
                return True


class SudokuBoardTests(unittest.TestCase):
    EASY = [("..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..",
             "483921657967345821251876493548132976729564138136798245372689514814253769695417382")]

    HARD = [("4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......",
             "417369825632158947958724316825437169791586432346912758289643571573291684164875293")]

    def setUp(self):
        pass

    def test_init(self):
        self.assertEqual(81, len(SudokuBoard().initial_state))
        self.assertEqual(SudokuBoard.EMPTY_BOARD, SudokuBoard().initial_state)
        self.assertFalse(SudokuBoard().is_solved())

    def test_cells(self):
        b = SudokuBoard()
        self.assertEqual(81, len(b.cells))
        self.assertEqual('A1', b.cells[0].name)
        self.assertEqual('C6', b.cells[23].name)
        self.assertEqual('I9', b.cells[80].name)

    def test_units(self):
        b = SudokuBoard()
        self.assertTrue(all(len(c.units) == 3 for c in b.cells))
        c2 = b.cell_by_name('C2')
        self.assertEqual(b.cell_by_name('A2'), c2.units[0][0])
        self.assertEqual(b.cell_by_name('C3'), c2.units[1][2])
        self.assertEqual(b.cell_by_name('C3'), c2.units[2][8])

    def test_peers(self):
        b = SudokuBoard()
        self.assertTrue(all(len(c.peers) == 20 and c not in c.peers for c in b.cells))

    def test_solve_easy(self):
        for puzzle, answer in self.EASY:
            b = SudokuBoard(puzzle)
            b.solve()
            self.assertTrue(b.is_solved())
            self.assertEqual(answer, b.state)

    def test_solve_hard(self):
        for puzzle, answer in self.HARD:
            b = SudokuBoard(puzzle)
            b.solve()
            self.assertTrue(b.is_solved())
            self.assertEqual(answer, b.state)

    def tearDown(self):
        pass

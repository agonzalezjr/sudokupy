import unittest
import collections


class SudokuCell:
    """
    A cell in a Sudoku puzzle board.
    """

    def __init__(self, name, choices=9):
        """
        Creates a Sudoku Cell
        :param name: the name of the cell (row-column)
        :param choices: the number of choices the cell can have
        :return: SudokuCell
        """
        assert (name is not None and len(name) == 2)
        self.__name = name
        # string with value '1..choices'
        self.__values = ''.join(str(d) for d in range(1, choices + 1))
        self.__peers = set()
        self.__units = []

    def __repr__(self):
        """Row-Column name of the cell (e.g. A1, C7, etc...)"""
        return self.name

    @property
    def name(self):
        """
        Row-Column name of the cell (e.g. A1, C7, etc...)

        :returns: name of the cell
        :rtype: str
        """
        return self.__name

    @property
    def values(self):
        return self.__values

    @property
    def peers(self):
        return self.__peers

    @property
    def units(self):
        return self.__units

    def __add_peers(self, p):
        """
        Adds other cell peers to this cell
        :param p: iterable collection of cells or a single cell to add as a peer
        """
        if isinstance(p, collections.Iterable):
            map(self.__add_peers, p)
        elif isinstance(p, self.__class__):
            if self.__name != p.name:
                # can't be a peer to itself
                self.__peers.add(p)

    def add_unit(self, u):
        self.__units.append(u)
        self.__add_peers(u)

    def eliminate(self, value):
        """
        Eliminates a value from the possible values of this cell.
        If after doing the elimination, it checks the cell's units, and
        if the value is only possible in one cell in the whole unit,
        it will assign it to that cell.
        :param value:
        :return: False if a contradiction is found
        """
        assert (len(value) == 1)

        # Contradiction: can't eliminate the last value!
        if self.values == value:
            return False

        # We already had this information, no need to propagate this further
        if value not in self.values:
            return True

        self.__values = self.values.replace(value, '')

        # Check this cell's units, if there is only one
        # possibility for the eliminated value now, then assign
        # the value to that lucky cell
        for unit in self.units:
            # d_places is an array of all the cells in the unit
            # that aren't solved already where the value is a possibility
            d_places = [cell for cell in unit if value in cell.values]
            if len(d_places) == 0:
                # Contradiction: there is no place for this value!
                return False
            elif len(d_places) == 1 and not d_places[0].is_solved():
                # We have only one choice and it's not because it's in
                # a cell we already solved. Yay for new information!!
                return d_places[0].assign(value)

        return True

    def assign(self, value):
        """
        Assigns a value to a cell.
        :param value: Either the initial value or a deduced one, but it will be the
        final value of the cell.
        It will then eliminate this value from all of this cell's peers as well.
        :return: False if there is a contradiction
        """
        assert (len(value) == 1)

        # Contradiction: Can't assign a value that's not a possibility!
        if value not in self.values:
            return False

        # We already had this information, no need to propagate anything
        if self.values == value:
            return True

        self.__values = value

        # We can eliminate this value from all of this cell's peers
        for peer in self.peers:
            if not peer.eliminate(value):
                # There was a problem eliminating this value
                # from the peers, so the assignation was wrong
                return False

        # All was good assigning this value to this call
        return True

    def is_solved(self):
        """ Returns true if the cell is solved """
        return len(self.values) == 1


class SudokuCellTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        c = SudokuCell('A1')
        self.assertEqual('A1', c.name)
        self.assertEqual('123456789', c.values)
        self.assertEqual(0, len(c.peers))

    def test_values(self):
        c = SudokuCell('A1')
        self.assertFalse(c.is_solved())

        c.eliminate('1')
        self.assertEqual('23456789', c.values)
        c.eliminate('1')
        self.assertEqual('23456789', c.values)
        c.eliminate('4')
        self.assertEqual('2356789', c.values)
        c.eliminate('9')
        self.assertEqual('235678', c.values)
        self.assertFalse(c.is_solved())

        self.assertFalse(c.assign('9'))
        self.assertFalse(c.is_solved())

        c.assign('6')
        self.assertTrue(c.is_solved())
        self.assertEqual('6', c.values)

        c.eliminate('5')
        self.assertEqual('6', c.values)
        self.assertFalse(c.eliminate('6'))

    def test_units(self):
        c = SudokuCell('A1')
        self.assertTrue(len(c.units) == 0)

        c.add_unit([c, c])
        self.assertTrue(len(c.units) == 1)

    def test_peers(self):
        c = SudokuCell('A1')
        p1 = SudokuCell('B1')

        c.add_unit([p1])
        self.assertTrue(p1 in c.peers)

        p2 = SudokuCell('B2')
        p3 = SudokuCell('B3')
        c.add_unit([p2, p3])
        self.assertTrue(p2 in c.peers)
        self.assertTrue(p3 in c.peers)

        self.assertTrue(c not in c.peers)
        self.assertTrue(p1 not in p1.peers)
        self.assertTrue(p2 not in p2.peers)
        self.assertTrue(p3 not in p3.peers)

    def tearDown(self):
        pass

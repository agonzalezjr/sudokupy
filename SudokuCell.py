import unittest
import collections


class SudokuCell:
    def __init__(self, name, choices=9):
        assert (name is not None and len(name) == 2)
        self.__name = name
        self.__values = ''.join(str(d) for d in range(1, choices + 1))
        self.__peers = set()
        self.__units = []

    def __repr__(self):
        return self.__name

    @property
    def name(self):
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
        assert (len(value) == 1)

        # Can't eliminate the last value
        if self.values == value:
            return False

        self.__values = self.values.replace(value, '')

        # Check this cell's units, if there is only one
        # possibility for some value there now, then assign
        # that value to that lucky cell
        for unit in self.units:
            for d in '123456789':
                # d_places is an array of all the cells in the unit
                # that aren't solved already where value d is a possibility
                d_places = [cell for cell in unit if d in cell.values]
                if len(d_places) == 0:
                    # Contradiction: no place for this value
                    return False
                elif len(d_places) == 1 and not d_places[0].is_solved():
                    # We have only one choice and it's not because it's in
                    # a cell we already solved. Yay for new information!!
                    return d_places[0].assign(d)

        return True

    def assign(self, value):
        assert (len(value) == 1)

        # Can't assign a value that's not a possibility
        if value not in self.values:
            return False

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

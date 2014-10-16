import unittest

# TODO: Make this a 'hashable' object using the name as the hash

class SudokuCell:
    def __init__(self, name, choices = 9):
        assert(name is not None and len(name) == 2)
        self.__name = name
        self.__values = ''
        for i in range(1, choices + 1):
            self.__values += str(i)

    @property
    def name(self):
        return self.__name

    @property
    def values(self):
        return self.__values

    def eliminate(self, value):
        assert (len(value) == 1)

        # Can't eliminate the last value
        if self.values == value:
            return False

        self.values = self.values.replace(value, '')

        # Yes, we can have different return values for one function
        return self.values

    def assign(self, value):
        assert (len(value) == 1)

        # Can't assign a value that's not a possibility
        if value not in self.values:
            return False

        self.values = value
        # no return value: means return 'None'

    def is_solved(self):
        return len(self.values) == 1


class SudokuCellTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        c = SudokuCell('A1')
        self.assertEqual(c.name, 'A1')
        self.assertEqual(c.values, '123456789')

    def test_values(self):
        c = SudokuCell('A1')
        self.assertFalse(c.is_solved())

        self.assertEqual('23456789', c.eliminate('1'))
        self.assertEqual('23456789', c.eliminate('1'))
        self.assertEqual('2356789', c.eliminate('4'))
        self.assertEqual('235678', c.eliminate('9'))
        self.assertFalse(c.is_solved())

        self.assertFalse(c.assign('9'))
        self.assertFalse(c.is_solved())

        c.assign('6')
        self.assertTrue(c.is_solved())
        self.assertEqual('6', c.values)

        self.assertEqual('6', c.eliminate('5'))
        self.assertFalse(c.eliminate('6'))

    def tearDown(self):
        pass

import unittest


class SudokuCell:
    def __init__(self, name):
        assert(name is not None and len(name) == 2)
        self.__name = name
        self.__choices = set(range(1, 10))

    @property
    def name(self):
        return self.__name

    @property
    def choices(self):
        return self.__choices

    def is_solved(self):
        return len(self.choices) == 1


class SudokuCellTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        c = SudokuCell('A1')
        self.assertEqual(c.name, 'A1')
        self.assertEqual(len(c.choices), 9)
        for d in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            self.assertTrue(d in c.choices)

    def test_solve(self):
        c = SudokuCell('A1')
        self.assertFalse(c.is_solved())

    def tearDown(self):
        pass

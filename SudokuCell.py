import unittest

# TODO: Make this a 'hashable' object

class SudokuCell:
    def __init__(self, name, choices = 9):
        assert(name is not None and len(name) == 2)
        self.__name = name
        self.__choices = ''
        for i in range(1, choices + 1):
            self.__choices += str(i)

    @property
    def name(self):
        return self.__name

    @property
    def choices(self):
        return self.__choices


class SudokuCellTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        c = SudokuCell('A1')
        self.assertEqual(c.name, 'A1')
        self.assertEqual(c.choices, '123456789')

    def tearDown(self):
        pass

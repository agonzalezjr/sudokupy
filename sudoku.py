import unittest

class SudokuBoard :
	def __init__(self, initString = None):
		if initString == None:
			self.__initString = "................................................................................."
		else:
			# Could do some more validation
			self.__initString = initString;

	def initString(self):
		return self.__initString

def fun(x):
	return x + 1

class SudokuBoardTests(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def testInit(self):
		self.assertEqual(SudokuBoard().initString(), ".................................................................................")

	def tearDown(self):
		pass


if __name__ == "__main__":
	s = SudokuBoard()
	print s.initString()

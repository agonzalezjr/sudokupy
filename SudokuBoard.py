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

    def prettyInitString(self):
        pass

    def printNice(self ) :
        """ Prints the SudokPuzzle to STDOUT in a nice table format """
        print "+---"*9 + "+"
        for i in range( 0, 9 ) :
            print "|", " | ".join( [ str( c ) for c in self.__initString[i] ] ), "|"
            print "+---"*9 + "+"

class SudokuBoardTests(unittest.TestCase):

    def setUp(self):
        pass

    def testInit(self):
        self.assertEqual(SudokuBoard().initString(), ".................................................................................")

    def testPretty(self):
        pass

    def testAnotherthing(self):
        pass

    def tearDown(self):
        pass

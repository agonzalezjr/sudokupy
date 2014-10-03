
"""
Just diving into python ... a couple of classes to represent and solve
a Sudoku puzzle using python ...
"""

from SudokuCell import SudokuCell

class SudokuBoard :
    # Class constants - Is there a better way for this in python?
    SIZE = 9
    
    def __init__( self, initString = None ):
        """Initializes a new sudoku board with 9x9 array of new cells"""
        self.__solvedCells = [ ]
        self.__table = [ ]

        if len( initString ) != SudokuBoard.SIZE * SudokuBoard.SIZE :
            initString = None
        
        for r in range( 0, 9 ) :
            row = [ ]
            for c in range( 0, 9 ) :
                if initString != None and initString[ r * SudokuBoard.SIZE + c ] != '?' :
                    cell = SudokuCell( r, c, initString[ r * SudokuBoard.SIZE + c ] )
                    row.append( cell )
                    self.__solvedCells.append( cell )
                else :
                    row.append( SudokuCell( r, c ) )
            self.__table.append( row )
            
    def isSolved( self ) :
        return len( self.__solvedCells ) == SudokuBoard.SIZE * SudokuBoard.SIZE 
    
    def solve( self ) :
    	""" This is where the magic happens """
    	pass;

    def printNice(self ) :
    	""" Prints the SudokPuzzle to STDOUT in a nice table format """
    	print "+---"*9 + "+"
        for i in range( 0, 9 ) :
            print "|", " | ".join( [ str( c ) for c in self.__table[i] ] ), "|"
            print "+---"*9 + "+"
            
    def printPosibilities( self ) :
    	""" Similar to the one above, but it prints each cell's possibilities """
        sep = ( "|" + "-" * 9 ) * 9 + "|"
        print sep
        for i in range( 0, 9 ) :
            print "|" + "|".join( [  c.getPosString( ) for c in self.__table[ i ] ] ) + "|"
            print sep
    
if __name__ == "__main__":
    # No IO for now, just testing the prints and creation paths
    s = SudokuBoard( "?9??1?3?26?1???????2?8???91238?????74????8??3????3185?9????2?3???2??5?493?549??2?" )
    s.printNice( )
    s.printPosibilities( )

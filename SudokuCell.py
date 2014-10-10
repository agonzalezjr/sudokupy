
class SudokuCell :
    def __init__( self, row, col, initValue = None ) :
        """ Represents a cell in a sudoku puzzle.
            Hey!
        Initializes a new sudoku cell, all posibilities are there
            The possible values are actually kept as a set of values from [1..9] """
        self.__initValue = initValue # If the cell is not "solved" this value will be None
        self.__row = row # The row and column of the cell in the puzzle
        self.__col = col # The row and column are immutable
    # __pos is the possible values the cell could take
        if self.__initValue != None :
            self._pos = set( [ int( self.__initValue ) ] )
        else :
            self._pos = set( range( 1, 10 ) )
        
    def isSolved( self ) :
        return len( self._pos ) == 1    
    
    def solve( self, value ) :
        self._pos = set( [ value ] )    
    
    def reducePos( self, value ) :
        """ Given a value, it reduces it from the possible ones """
        self._pos = self._pos.difference( set( [ value ] ) )
        
    def getPosition( self ) :
        """ Position is just a tuple containig the cell's row and column """
        return ( self.__row, self.__col )
    
    def getBigCell( self ) :
        """ BigCell is the 3x3 group this cell belongs to. This returns its position """
        return ( self.__row / 3, self.__col / 3 )
    
    def getNeighborsPositions( self ) :
        """ Return a list containig the neighbors' positions
        Neighbors are other cells in the same row, column, or BigCell """
        np = [ ]
        
        # get neigbohrs in the same row
        for c in range( 0, 9 ) :
            if c == self.__col : continue
            np.append( ( self.__row, c ) )
        
        # get neighbors in the same column
        for r in range( 0, 9 ) :
            if r == self.__row : continue
            np.append( ( r, self.__col ) )
        
        # get neibohrs in the same cell
        cell = self.getBigCell( )
        for r in range( 3 * cell[ 0 ], 3 * cell[ 0 ] + 3 ) :
            for c in range( 3 * cell[ 1 ], 3 * cell[ 1 ] + 3 ) :
                if ( r, c ) != self.getPosition( ) and np.count( ( r, c ) ) == 0 :
                    np.append( ( r, c ) )
                        
        return np
            
    def getValue( self ) :
        if self.isSolved( ) :
            return int( self.__str__( ) )
        else :
            return None
        
    def getPosString( self ) :
        """ Returns a string containing the posibilities still available in this cell """
        ps = ""
        for i in range( 1, 10 ) :
            if i in self._pos :
                ps += str( i )
            else :
                ps += "x"
        return ps
            
        
    def __str__( self ) :
        """ Returns the string representation of the cell. If solve this is the value,
        if not solved, this is just '?' """
        if self.isSolved( ) :
            sol = self._pos.pop( )
            self._pos.add( sol )
            return str( sol )
        else :
            return '?'
    

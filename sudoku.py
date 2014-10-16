from SudokuBoard import SudokuBoard

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

if __name__ == "__main__":
    s = SudokuBoard("..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..")
    print s.initial_state
    print s.pretty()
    print s.pretty_values()



    # digits   = '123456789'
    # rows     = 'ABCDEFGHI'
    # cols     = digits
    # squares  = cross(rows, cols)
    # unitlist = ([cross(rows, c) for c in cols] +
    #             [cross(r, cols) for r in rows] +
    #             [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
    # units = dict((s, [u for u in unitlist if s in u])
    #              for s in squares)
    # peers = dict((s, set(sum(units[s],[]))-set([s]))
    #              for s in squares)

    print "done"

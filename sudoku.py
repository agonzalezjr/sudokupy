from SudokuBoard import SudokuBoard

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

if __name__ == "__main__":
    s = SudokuBoard("..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..")
    print s.initial_state
    print s.pretty_initial_state()

    debug_mode = True
    s.solve(debug_mode)

    print "done"

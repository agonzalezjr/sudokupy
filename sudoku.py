from SudokuBoard import SudokuBoard

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

if __name__ == "__main__":

    easy = SudokuBoard("..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..")
    print "This is an easy puzzle ..."
    print easy.pretty_initial_state()
    easy.solve()
    print easy.pretty()
    print "done"

    hard = SudokuBoard("4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......")
    print "This is a very HARD puzzle ..."
    print hard.pretty_initial_state()
    hard.solve()
    print hard.pretty_values()
    print "done"

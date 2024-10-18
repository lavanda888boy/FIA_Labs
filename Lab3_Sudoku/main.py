from sudoku_solver import SudokuSolver

ss = SudokuSolver('./grid5.txt')

if __name__ == "__main__":
    ss.print_board()
    ss.solve()
    ss.print_board()

    # print(ss.domains)
    # print()
    # ss.propagate_constraints()
    # print(ss.domains)

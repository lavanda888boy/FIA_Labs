from sudoku_solver import SudokuSolver
from sudoku_validator import SudokuValidator

ss = SudokuSolver('./sudoku.txt')
sv = SudokuValidator(ss)

if __name__ == "__main__":
    ss.print_board()

    if sv.verify_board():
        ss.solve_advanced()
        ss.print_board()
    else:
        print("\nInvalid board.")

    # print(ss.domains)
    # print()
    # ss.propagate_constraints()
    # print(ss.domains)

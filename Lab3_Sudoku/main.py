from sudoku_solver import SudokuSolver
from sudoku_validator import SudokuValidator
from sudoku_generator import SudokuGenerator

if __name__ == "__main__":
    sg = SudokuGenerator()

    sg.solver.board = sg.generate_sudoku()

    sg.solver.print_board()
    # sg.solver.solve_advanced()
    # sg.solver.print_board()

    # ss.print_board()

    # if sv.verify_board():
    #     ss.solve_advanced()
    #     ss.print_board()
    # else:
    #     print("\nInvalid board.")

    # print(ss.domains)
    # print()
    # ss.propagate_constraints()
    # print(ss.domains)

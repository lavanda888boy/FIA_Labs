import random
from sudoku_solver import SudokuSolver
from sudoku_validator import SudokuValidator


class SudokuGenerator:

    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.solver = SudokuSolver(self.board, None)
        self.validator = SudokuValidator(self.solver)

    def generate_full_board(self):
        self.solver.solve_advanced()
        self.board = self.solver.board

    def remove_numbers(self, num_holes):
        count = 0

        while count < num_holes:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count += 1

    def generate_sudoku(self, num_holes=40):
        self.generate_full_board()

        while True:
            board_copy = [row.copy() for row in self.board]
            self.remove_numbers(num_holes)

            print(self.validator.check_multiple_solutions())

            if self.validator.check_multiple_solutions():
                return self.board
            else:
                self.board = board_copy
                self.validator.sudoku_solver.board = self.board

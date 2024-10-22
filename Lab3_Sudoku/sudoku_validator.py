from sudoku_solver import SudokuSolver


class SudokuValidator:

    minimal_givens = 17

    def __init__(self, sudoku_solver: SudokuSolver):
        self.sudoku_solver = sudoku_solver
        self.board = sudoku_solver.board
        self.domains = sudoku_solver.domains

        self.sudoku_solver.propagate_constraints()

    def verify_board(self):
        empty_board_check, empty_board_msg = self.check_empty_board()
        single_given_check, single_given_msg = self.check_single_given()
        insufficient_givens_check, insufficient_givens_msg = self.check_insufficient_givens()
        duplicates_check, duplicates_msg = self.check_duplicates()
        square_solvability_check, square_solvability_msg = self.check_unsolvable_square()
        box_column_row_solvability_check, box_column_row_solvability_msg = self.check_unsolvable_box_column_row()
        check_multiple_solutions, multiple_solutions_msg = self.check_multiple_solutions()

        print(empty_board_msg, single_given_msg, insufficient_givens_msg, duplicates_msg,
              square_solvability_msg, box_column_row_solvability_msg, multiple_solutions_msg)

        sudoku_validity_checks = empty_board_check and single_given_check and \
            insufficient_givens_check and duplicates_check and square_solvability_check and \
            box_column_row_solvability_check and check_multiple_solutions

        return sudoku_validity_checks

    def check_empty_board(self):
        if not all(cell == 0 for row in self.board for cell in row):
            return True, ""

        return False, "The board is empty."

    def check_single_given(self):
        given_count = sum(cell != 0 for row in self.board for cell in row)

        if given_count == 1:
            return False, "Only one given value."

        return True, ""

    def check_insufficient_givens(self):
        given_count = sum(cell != 0 for row in self.board for cell in row)

        if given_count < 17:
            return False, "Insufficient givens (less than 17)."

        return True, ""

    def check_duplicates(self):
        for i in range(9):
            row_values = [self.board[i][j]
                          for j in range(9) if self.board[i][j] != 0]

            if len(row_values) != len(set(row_values)):
                return False, f"Duplicate values found in row {i + 1}."

            col_values = [self.board[j][i]
                          for j in range(9) if self.board[j][i] != 0]

            if len(col_values) != len(set(col_values)):
                return False, f"Duplicate values found in column {i + 1}."

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box_values = [
                    self.board[r][c]
                    for r in range(box_row, box_row + 3)
                    for c in range(box_col, box_col + 3)
                    if self.board[r][c] != 0
                ]

                if len(box_values) != len(set(box_values)):
                    return False, f"Duplicate values found in 3x3 box starting at ({box_row + 1}, {box_col + 1})."

        return True, ""

    def check_unsolvable_square(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and len(self.domains[(i, j)]) == 0:
                    return False, f"Unsolvable square at ({i + 1}, {j + 1})."

        return True, ""

    def check_unsolvable_box_column_row(self):
        for num in range(1, 10):
            for i in range(9):
                if num not in [self.board[i][j] for j in range(9)]:
                    if not any(num in self.domains[(i, j)] for j in range(9) if self.board[i][j] == 0):
                        return False, f"Number {num} cannot be placed in row {i + 1}."

            for j in range(9):
                if num not in [self.board[i][j] for i in range(9)]:
                    if not any(num in self.domains[(i, j)] for i in range(9) if self.board[i][j] == 0):
                        return False, f"Number {num} cannot be placed in column {j + 1}."

            for box_row in range(0, 9, 3):
                for box_col in range(0, 9, 3):
                    if num not in [
                        self.board[r][c]
                        for r in range(box_row, box_row + 3)
                        for c in range(box_col, box_col + 3)
                    ]:
                        if not any(
                            num in self.domains[(r, c)]
                            for r in range(box_row, box_row + 3)
                            for c in range(box_col, box_col + 3)
                            if self.board[r][c] == 0
                        ):
                            return False, f"Number {num} cannot be placed in 3x3 box starting at ({box_row + 1}, {box_col + 1})."

        return True, ""

    def check_multiple_solutions(self):
        solution_count = self.sudoku_solver.solve_advanced(
            count_solutions=True)

        if solution_count > 1:
            return False, "Multiple solutions found."

        return True, "The board has a unique solution."

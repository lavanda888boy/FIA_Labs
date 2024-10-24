from sudoku_solver import solve_advanced

MINIMAL_GIVENS = 17


def verify_board(board, domains, neighbors):
    empty_board_check, empty_board_msg = check_empty_board(board)
    single_given_check, single_given_msg = check_single_given(board)
    insufficient_givens_check, insufficient_givens_msg = check_insufficient_givens(
        board)
    duplicates_check, duplicates_msg = check_duplicates(board)
    square_solvability_check, square_solvability_msg = check_unsolvable_square(
        board, domains)
    box_column_row_solvability_check, box_column_row_solvability_msg = check_unsolvable_box_column_row(
        board, domains)
    multiple_solutions_check, multiple_solutions_msg = check_multiple_solutions(
        board, domains, neighbors)

    print(empty_board_msg, single_given_msg, insufficient_givens_msg, duplicates_msg,
          square_solvability_msg, box_column_row_solvability_msg, multiple_solutions_msg)

    sudoku_validity_checks = empty_board_check and single_given_check and \
        insufficient_givens_check and duplicates_check and square_solvability_check and \
        box_column_row_solvability_check and multiple_solutions_check

    return sudoku_validity_checks


def check_empty_board(board):
    if not all(cell == 0 for row in board for cell in row):
        return True, ""

    return False, "The board is empty."


def check_single_given(board):
    given_count = sum(cell != 0 for row in board for cell in row)

    if given_count == 1:
        return False, "Only one given value."

    return True, ""


def check_insufficient_givens(board):
    given_count = sum(cell != 0 for row in board for cell in row)

    if given_count < 17:
        return False, "Insufficient givens (less than 17)."

    return True, ""


def check_duplicates(board):
    for i in range(9):
        row_values = [board[i][j]
                      for j in range(9) if board[i][j] != 0]

        if len(row_values) != len(set(row_values)):
            return False, f"Duplicate values found in row {i + 1}."

        col_values = [board[j][i]
                      for j in range(9) if board[j][i] != 0]

        if len(col_values) != len(set(col_values)):
            return False, f"Duplicate values found in column {i + 1}."

    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box_values = [
                board[r][c]
                for r in range(box_row, box_row + 3)
                for c in range(box_col, box_col + 3)
                if board[r][c] != 0
            ]

            if len(box_values) != len(set(box_values)):
                return False, f"Duplicate values found in 3x3 box starting at ({box_row + 1}, {box_col + 1})."

    return True, ""


def check_unsolvable_square(board, domains):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0 and len(domains[(i, j)]) == 0:
                return False, f"Unsolvable square at ({i + 1}, {j + 1})."

    return True, ""


def check_unsolvable_box_column_row(board, domains):
    for num in range(1, 10):
        for i in range(9):
            if num not in [board[i][j] for j in range(9)]:
                if not any(num in domains[(i, j)] for j in range(9) if board[i][j] == 0):
                    return False, f"Number {num} cannot be placed in row {i + 1}."

        for j in range(9):
            if num not in [board[i][j] for i in range(9)]:
                if not any(num in domains[(i, j)] for i in range(9) if board[i][j] == 0):
                    return False, f"Number {num} cannot be placed in column {j + 1}."

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                if num not in [
                    board[r][c]
                    for r in range(box_row, box_row + 3)
                    for c in range(box_col, box_col + 3)
                ]:
                    if not any(
                        num in domains[(r, c)]
                        for r in range(box_row, box_row + 3)
                        for c in range(box_col, box_col + 3)
                        if board[r][c] == 0
                    ):
                        return False, f"Number {num} cannot be placed in 3x3 box starting at ({box_row + 1}, {box_col + 1})."

    return True, ""


def check_multiple_solutions(board, domains, neighbors):
    solution_count = solve_advanced(board, domains, neighbors,
                                    count_solutions=True)

    if solution_count > 1:
        return False, "Multiple solutions found."

    return True, ""

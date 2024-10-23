import random
from sudoku_solver import solve_backtrack, initialize_domains, initialize_neighbors
from sudoku_validator import check_multiple_solutions


def generate_full_board():
    board = [[0] * 9 for _ in range(9)]
    solve_backtrack(board)
    return board


def remove_numbers(board, num_holes):
    count = 0

    while count < num_holes:
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        if board[row][col] != 0:
            board[row][col] = 0
            count += 1


def generate_sudoku(num_holes=40):
    board = generate_full_board()

    while True:
        board_copy = [row.copy() for row in board]
        remove_numbers(board, num_holes)

        domains = initialize_domains(board)
        neighbors = initialize_neighbors()

        if check_multiple_solutions(board, domains, neighbors):
            return board
        else:
            board = board_copy

from sudoku_solver import load_sudoku, print_board, solve_backtrack, solve_advanced, initialize_domains, initialize_neighbors
from sudoku_validator import verify_board
from sudoku_generator import generate_sudoku

if __name__ == "__main__":
    # board = load_sudoku("sudoku.txt")
    board = generate_sudoku()
    print_board(board)

    domains = initialize_domains(board)
    neighbors = initialize_neighbors()

    # print(verify_board(board, domains, neighbors))

    domains = initialize_domains(board)
    neighbors = initialize_neighbors()

    solve_advanced(board, domains, neighbors)
    print_board(board)

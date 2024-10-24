from sudoku_solver import load_sudoku, print_board, solve_advanced, initialize_domains, initialize_neighbors, propagate_constraints_AC

if __name__ == "__main__":
    board = load_sudoku("./puzzles/grid4.txt")
    print_board(board)

    domains = initialize_domains(board)
    neighbors = initialize_neighbors()

    propagate_constraints_AC(board, domains, neighbors)
    solve_advanced(board, domains, neighbors)
    print_board(board)

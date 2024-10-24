ZERO_DELIMITER = '*'


def load_sudoku(file_path):
    board = []

    with open(file_path, 'r') as file:
        for line in file:
            row = [int(char) if char !=
                   ZERO_DELIMITER else 0 for char in line.strip()]
            board.append(row)

    return board


def print_board(board):
    for row in board:
        print(" ".join(str(num) for num in row))
    print()


def initialize_domains(board):
    domains = {}

    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                domains[(i, j)] = set(range(1, 10))
            else:
                domains[(i, j)] = {board[i][j]}

    return domains


def initialize_neighbors():
    neighbors = {}

    for row in range(9):
        for col in range(9):
            neighbors[(row, col)] = get_neighbors((row, col))

    return neighbors


def get_neighbors(var):
    row, col = var
    neighbors = set()

    for i in range(9):
        if (row, i) != var:
            neighbors.add((row, i))
        if (i, col) != var:
            neighbors.add((i, col))

    box_x = col // 3
    box_y = row // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if (i, j) != var:
                neighbors.add((i, j))

    return neighbors


def propagate_constraints(domains, board):
    for domain_key in domains.keys():
        if board[domain_key[0]][domain_key[1]] == 0:
            for num in range(1, 10):
                if not is_valid_number(num, domain_key, board):
                    domains[domain_key].discard(num)


def propagate_constraints_AC(board, domains, neighbors):
    queue = [(var, neighbor)
             for var in domains for neighbor in get_neighbors(var)]
    while queue:
        (xi, xj) = queue.pop(0)

        if revise(xi, xj, board, domains, neighbors):
            if len(domains[xi]) == 0:
                return False

            for xk in get_neighbors(xi):
                if xk != xj:
                    queue.append((xk, xi))


def revise(xi, xj, board, domains, neighbors):
    revised = False

    for x in set(domains[xi]):
        if not any(is_valid_number(x, (xi[0], xi[1]), board) for xi in neighbors[xj]):
            domains[xi].remove(x)
            revised = True

    return revised


def forward_checking(row, col, num, domains):
    for i in range(9):
        if (row, i) in domains:
            domains[(row, i)].discard(num)
        if (i, col) in domains:
            domains[(i, col)].discard(num)

    box_x = col // 3
    box_y = row // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if (i, j) in domains:
                domains[(i, j)].discard(num)


def is_valid_number(num, pos, board):
    row, col = pos

    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num:
                return False

    return True


def find_empty_cell(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)

    return None


def find_empty_cell_mrv(domains, board):
    min_domain_size = float('inf')
    best_cell = None

    for cell in domains:
        if board[cell[0]][cell[1]] == 0:
            domain_size = len(domains[cell])

            if domain_size < min_domain_size:
                min_domain_size = domain_size
                best_cell = cell

    return best_cell


def order_domains_lcv(var, domains):
    def count_constraints(value):
        count = 0
        row, col = var

        for i in range(9):
            if (row, i) in domains and value in domains[(row, i)]:
                count += 1

        for i in range(9):
            if (i, col) in domains and value in domains[(i, col)]:
                count += 1

        box_x = col // 3
        box_y = row // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if (i, j) in domains and value in domains[(i, j)]:
                    count += 1

        return count

    return sorted(domains[var], key=count_constraints)


def solve_backtrack(board):
    empty_cell = find_empty_cell(board)

    if not empty_cell:
        return True
    else:
        row, col = empty_cell

    for i in range(1, 10):
        if is_valid_number(i, (row, col), board):
            board[row][col] = i

            if solve_backtrack(board):
                return True

            board[row][col] = 0

    return False


def solve_advanced(board, domains, neighbors, count_solutions=False):
    empty_cell = find_empty_cell_mrv(domains, board)

    if not empty_cell:
        return 1 if count_solutions else True

    row, col = empty_cell
    solution_count = 0

    for num in order_domains_lcv((row, col), domains):
        if is_valid_number(num, (row, col), board):
            board[row][col] = num
            local_domains = {key: value.copy()
                             for key, value in domains.items()}
            forward_checking(row, col, num, domains)

            if count_solutions:
                solution_count += solve_advanced(board,
                                                 domains, neighbors, count_solutions)
                if solution_count > 1:
                    return solution_count
            else:
                if solve_advanced(board,
                                  domains, neighbors):
                    return True

            board[row][col] = 0
            domains = local_domains

    return solution_count if count_solutions else False

class SudokuSolver:

    zero_delimiter = '*'

    def __init__(self, file_path):
        self.board = []

        with open(file_path, 'r') as file:
            for line in file:
                row = [int(char) if char !=
                       self.zero_delimiter else 0 for char in line.strip()]
                self.board.append(row)

        self.domains = self.initialize_domains()
        self.neighbors = self.initialize_neighbors()

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) for num in row))
        print()

    def initialize_domains(self):
        domains = {}

        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    domains[(i, j)] = set(range(1, 10))
                else:
                    domains[(i, j)] = {self.board[i][j]}

        return domains

    def initialize_neighbors(self):
        neighbors = {}

        for row in range(9):
            for col in range(9):
                neighbors[(row, col)] = self.get_neighbors((row, col))

        return neighbors

    def get_neighbors(self, var):
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

    def propagate_constraints(self):
        for domain_key in self.domains.keys():
            if self.board[domain_key[0]][domain_key[1]] == 0:
                for num in range(1, 10):
                    if not self.is_valid_number(num, domain_key):
                        self.domains[domain_key].discard(num)

    def propagate_constraints_AC(self):
        queue = [(var, neighbor)
                 for var in self.domains for neighbor in self.get_neighbors(var)]
        while queue:
            (xi, xj) = queue.pop(0)

            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False

                for xk in self.get_neighbors(xi):
                    if xk != xj:
                        queue.append((xk, xi))

    def revise(self, xi, xj):
        revised = False

        for x in set(self.domains[xi]):
            if not any(self.is_valid_number(x, (xi[0], xi[1])) for xi in self.neighbors[xj]):
                self.domains[xi].remove(x)
                revised = True

        return revised

    def forward_checking(self, row, col, num):
        for i in range(9):
            if (row, i) in self.domains:
                self.domains[(row, i)].discard(num)
            if (i, col) in self.domains:
                self.domains[(i, col)].discard(num)

        box_x = col // 3
        box_y = row // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if (i, j) in self.domains:
                    self.domains[(i, j)].discard(num)

    def is_valid_number(self, num, pos):
        row, col = pos

        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        box_x = col // 3
        box_y = row // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def find_empty_cell(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return (i, j)

        return None

    def find_empty_cell_mrv(self):
        min_domain_size = float('inf')
        best_cell = None

        for cell in self.domains:
            if self.board[cell[0]][cell[1]] == 0:
                domain_size = len(self.domains[cell])

                if domain_size < min_domain_size:
                    min_domain_size = domain_size
                    best_cell = cell

        return best_cell

    def order_domains_lcv(self, var):
        def count_constraints(value):
            count = 0
            row, col = var

            for i in range(9):
                if (row, i) in self.domains and value in self.domains[(row, i)]:
                    count += 1

            for i in range(9):
                if (i, col) in self.domains and value in self.domains[(i, col)]:
                    count += 1

            box_x = col // 3
            box_y = row // 3

            for i in range(box_y * 3, box_y * 3 + 3):
                for j in range(box_x * 3, box_x * 3 + 3):
                    if (i, j) in self.domains and value in self.domains[(i, j)]:
                        count += 1

            return count

        return sorted(self.domains[var], key=count_constraints)

    def solve_backtrack(self):
        empty_cell = self.find_empty_cell()

        if not empty_cell:
            return True
        else:
            row, col = empty_cell

        for i in range(1, 10):
            if self.is_valid_number(i, (row, col)):
                self.board[row][col] = i

                if self.solve_backtrack():
                    return True

                self.board[row][col] = 0

        return False

    def solve_advanced(self, count_solutions=False):
        empty_cell = self.find_empty_cell_mrv()

        if not empty_cell:
            return 1 if count_solutions else True

        row, col = empty_cell
        solution_count = 0

        for num in self.order_domains_lcv((row, col)):
            if self.is_valid_number(num, (row, col)):
                self.board[row][col] = num
                # self.propagate_constraints()
                self.propagate_constraints_AC()
                self.forward_checking(row, col, num)

                if count_solutions:
                    solution_count += self.solve_advanced(count_solutions)
                    if solution_count > 1:
                        return solution_count
                else:
                    if self.solve_advanced():
                        return True

                self.board[row][col] = 0
                self.domains = self.initialize_domains()
                # self.propagate_constraints()
                self.propagate_constraints_AC()

        return solution_count if count_solutions else False

class SudokuSolver:

    def __init__(self, file_path):
        self.board = []

        with open(file_path, 'r') as file:
            for line in file:
                row = [int(char) if char !=
                       '*' else 0 for char in line.strip()]
                self.board.append(row)

        self.domains = self.initialize_domains()

    def initialize_domains(self):
        domains = {}

        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    domains[(i, j)] = set(range(1, 10))
                else:
                    domains[(i, j)] = {self.board[i][j]}

        return domains

    def propagate_constraints(self):
        for domain_key in self.domains.keys():
            if self.board[domain_key[0]][domain_key[1]] == 0:
                for num in range(1, 10):
                    if not self.is_valid(num, domain_key):
                        self.domains[domain_key].discard(num)

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

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) for num in row))
        print()

    def is_valid(self, num, pos):
        for i in range(len(self.board[0])):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False

        for i in range(len(self.board)):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
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

    def solve(self):
        # empty_cell = self.find_empty_cell()
        empty_cell = self.find_empty_cell_mrv()

        if not empty_cell:
            return True

        row, col = empty_cell

        # for num in list(self.domains[(row, col)]):
        for num in self.order_domains_lcv((row, col)):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                self.propagate_constraints()
                self.forward_checking(row, col, num)

                if self.solve():
                    return True

                self.board[row][col] = 0
                self.domains = self.initialize_domains()
                self.propagate_constraints()

        return False

class SudokuSolver:

    def __init__(self, file_path):
        self.board = []

        with open(file_path, 'r') as file:
            for line in file:
                row = [int(char) if char !=
                       '*' else 0 for char in line.strip()]
                self.board.append(row)

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

    def solve(self):
        empty_cell = self.find_empty_cell()

        if not empty_cell:
            return True
        else:
            row, col = empty_cell

        for i in range(1, 10):
            if self.is_valid(i, (row, col)):
                self.board[row][col] = i

                if self.solve():
                    return True

                self.board[row][col] = 0

        return False

from copy import deepcopy as copy
import argparse
from animation import draw


class Node():
    def __init__(self, board, jumpfrom=None, jumpover=None, jumpto=None):
        self.board = board
        self.jumpfrom = jumpfrom
        self.jumpover = jumpover
        self.jumpto = jumpto


class peg:
    def __init__(self, start_row, start_col, rule):
        self.size = 5
        self.start_row, self.start_col, self.rule = start_row, start_col, rule
        # board
        self.board = [[1 for j in range(i + 1)] for i in range(self.size)]
        self.board[start_row][start_col] = 0
        self.start = Node(copy(self.board))
        # path
        self.path = [self.start]
        # Do some initialization work here if you need:

    def draw(self):
        if self.success():
            draw(self.path, self.start_row, self.start_col, self.rule)
        else:
            print("No solution were found!")

    def success(self):
        total = 0
        for row in self.board:
            total += sum(row)
        if total == 1:
            if self.rule == 1 and self.path[-1].jumpto != (self.start_row, self.start_col):
                return False
            return True
        return False

    def get_successors(self):
        direction_rows = [-2, -2, 2, 2, 0, 0]
        direction_columns = [0, -2, 0, 2, -2, 2]
        jumps = []

        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                for k in range(6):

                    # Check if jump is in boundary
                    if not (0 <= row + direction_rows[k] < len(self.board) and 0 <= column + direction_columns[k] <
                            len(self.board[row + direction_rows[k]])):
                        continue

                    # Check that jump_from is a peg
                    jump_from = (row, column)
                    if self.board[row][column] != 1:
                        continue

                    # Check that jump_over is a peg
                    jump_over = (row + int(direction_rows[k] / 2), column + int(direction_columns[k] / 2))
                    if self.board[jump_over[0]][jump_over[1]] != 1:
                        continue

                    # Check that jump_to is a hole
                    jump_to = (row + direction_rows[k], column + direction_columns[k])
                    if self.board[jump_to[0]][jump_to[1]] != 0:
                        continue

                    new_board = copy(self.board)
                    new_board[jump_from[0]][jump_from[1]] = 0
                    new_board[jump_over[0]][jump_over[1]] = 0
                    new_board[jump_to[0]][jump_to[1]] = 1

                    jumps.append(Node(new_board, jump_from, jump_over, jump_to))

        return jumps

    def solve(self):
        if self.success():
            return True

        jumps = self.get_successors()

        for node in jumps:

            board_copy = copy(self.board)
            self.board = node.board
            self.path.append(node)

            if self.solve():
                return True

            self.board = board_copy
            self.path.pop()

        return False


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='peg game')

    parser.add_argument('-hole', dest='position', required=True, nargs='+', type=int,
                        help='initial position of the hole')
    parser.add_argument('-rule', dest='rule', required=True, type=int, help='index of rule')

    args = parser.parse_args()

    start_row, start_col = args.position
    if start_row > 4:
        print("row must be less or equal than 4")
        exit()
    if start_col > start_row:
        print("column must be less or equal than row")
        exit()

    # Example: 
    # python peg.py -hole 0 0 -rule 0
    game = peg(start_row, start_col, args.rule)
    game.solve()
    game.draw()

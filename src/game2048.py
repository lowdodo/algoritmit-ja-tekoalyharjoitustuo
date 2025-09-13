import random


class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.add_tile()
        self.add_tile()

    def add_tile(self):
        empty_tiles = [(row, colum) for row in range(self.size)
                       for colum in range(self.size) if self.board[row][colum] == 0]
        if empty_tiles:
            row, colum = random.choice(empty_tiles)
            self.board[row][colum] = 2 if random.random() < 0.9 else 4

    def slide_and_merge(self, row):
        new_row = [i for i in row if i != 0]
        merged_row = []
        skip = False
        for i in range(len(new_row)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
                merged_row.append(new_row[i] * 2)
                skip = True
            else:
                merged_row.append(new_row[i])
        merged_row += [0] * (self.size - len(merged_row))
        return merged_row

    def move_left(self):
        return [self.slide_and_merge(row) for row in self.board]

    def move_right(self):
        return [self.slide_and_merge(row[::-1])[::-1] for row in self.board]

    def move_up(self):
        transposed = list(zip(*self.board))
        merged = [self.slide_and_merge(list(row)) for row in transposed]
        return [list(row) for row in zip(*merged)]

    def move_down(self):
        transposed = list(zip(*self.board))
        merged = [self.slide_and_merge(list(row)[::-1])[::-1]
                  for row in transposed]
        return [list(row) for row in zip(*merged)]

    def is_game_over(self):
        for row in self.board:
            if 0 in row:
                return False
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.board[r][c] == self.board[r][c + 1]:
                    return False
        for c in range(self.size):
            for r in range(self.size - 1):
                if self.board[r][c] == self.board[r + 1][c]:
                    return False
        return True

    def check_win(self):
        return any(2048 in row for row in self.board)

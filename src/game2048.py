import random


class Game2048:
    ''' Class representing the 2048 game logic.
    
    Attributes:
        size (int): The size of the game board (size x size).
        board (list): The current state of the game board.
        directions (list): Possible move directions.
        score (int): The current score of the game.
        '''
    def __init__(self, size=4):
        '''Initializor for the 2048 game.'''
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.directions = ['left', 'right', 'up', 'down']
        self.score = 0
        self.add_tile()
        self.add_tile()

    def add_tile(self):
        ''' Add a new tile (2 or 4) to a random empty position on the board.
        uses original probabilities of 90% for 2 and 10% for 4'''
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

    def move(self, direction, add_tile=True):
        moved = False
        old_board = [row[:] for row in self.board]

        if direction == 'left':
            for r in range(self.size):
                new_row = self.slide_and_merge(self.board[r])
                if new_row != self.board[r]:
                    moved = True
                self.board[r] = new_row

        elif direction == 'right':
            for r in range(self.size):
                new_row = list(reversed(self.slide_and_merge(
                    list(reversed(self.board[r])))))
                if new_row != self.board[r]:
                    moved = True
                self.board[r] = new_row

        elif direction == 'up':
            for c in range(self.size):
                col = [self.board[r][c] for r in range(self.size)]
                new_col = self.slide_and_merge(col)
                if new_col != col:
                    moved = True
                for r in range(self.size):
                    self.board[r][c] = new_col[r]

        elif direction == 'down':
            for c in range(self.size):
                col = [self.board[r][c] for r in range(self.size)]
                new_col = list(
                    reversed(self.slide_and_merge(list(reversed(col)))))
                if new_col != col:
                    moved = True
                for r in range(self.size):
                    self.board[r][c] = new_col[r]

        if moved and add_tile:
            self.add_tile()

        return self.board, moved

    def is_game_over(self):
        ''' Check if no more moves are possible.'''
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

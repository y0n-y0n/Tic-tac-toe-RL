class Board:
    def __init__(self):
        self.grid = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]

    def display(self):
        for row in self.grid:
            print(" | ".join(row))
            print("-" * 9)
    def restart(self):
        self.grid = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]

    def available_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == ".":
                    moves.append((i, j))
        return moves

    def make_move(self,pos,mark):
        row, col = pos
        if self.grid[row][col] == ".":
            self.grid[row][col] = mark
            return True
        return False

    def winner(self):
        for row in self.grid:
            if row[0] == row[1] == row[2] != ".":
                return row[0]
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] != ".":
                return self.grid[0][col]
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != ".":
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != ".":
            return self.grid[0][2]
        return None
    
    def is_full(self):
        for row in self.grid:
            for cell in row:
                if cell == ".":
                    return False
        return True

    def is_over(self):
        if self.winner() is not None or self.is_full():
            return True
        return False
    
    def to_key(self):
        return tuple(cell for row in self.grid for cell in row)
    
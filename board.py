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

    # claude
    # All 8 lines as square indexes (index = row * 3 + col)
    LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6),             # diagonals
    ]

    def load(self, grid):
        """Replace the grid with a 3x3 list of lists. Returns False (and leaves
        the board unchanged) if the shape or a cell value is wrong."""
        if not isinstance(grid, list) or len(grid) != 3:
            return False
        for row in grid:
            if not isinstance(row, list) or len(row) != 3:
                return False
            for cell in row:
                if cell not in ("X", "O", "."):
                    return False
        self.grid = [list(row) for row in grid]
        return True

    def winning_line(self):
        """The 3 square indexes of a completed line, or None."""
        cells = self.to_key()
        for line in self.LINES:
            a, b, c = line
            if cells[a] == cells[b] == cells[c] != ".":
                return list(line)
        return None

    def is_legal(self):
        """True if this position can occur in a real game."""
        cells = self.to_key()
        if abs(cells.count("X") - cells.count("O")) > 1:
            return False
        winners = {cells[a] for a, b, c in self.LINES
                   if cells[a] == cells[b] == cells[c] != "."}
        return len(winners) < 2
    
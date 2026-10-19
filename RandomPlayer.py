
import random


class RandomPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def choose_move(self, board):
        move = random.choice(board.available_moves())
        board.make_move(move, self.symbol)
        return move

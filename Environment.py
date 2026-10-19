from board import Board
from RandomPlayer import RandomPlayer

class Environment:
    def __init__(self):
        self.board = Board()
        self.player1 = RandomPlayer("X")
        self.agentmark = "O"
        self.WIN_REWARD = 10
        self.LOSS_REWARD = -10
        self.DRAW_REWARD = 0
        self.MOVE_REWARD = 0
        self.ILLEGAL_REWARD = -1
        self.result = None
    def get_state(self):
        # flat, immutable copy of the board: cells 0-8, usable as a Q-table key
        return tuple(cell for row in self.board.grid for cell in row)
    def reset(self, agent_starts):
        self.board.restart()
        self.result = None
        if not agent_starts:
            self.player1.choose_move(self.board)
        return self.get_state()
    def step(self, action):
        # action is a cell index 0-8 -> (row, col)
        pos = divmod(action, 3)
        if not self.board.make_move(pos, self.agentmark):
            return self.get_state(), self.ILLEGAL_REWARD, False
        if self.board.winner() == self.agentmark:
            self.result = "win"
            return self.get_state(), self.WIN_REWARD, True
        if self.board.is_full():
            self.result = "draw"
            return self.get_state(), self.DRAW_REWARD, True
        self.player1.choose_move(self.board)
        if self.board.winner() == self.player1.symbol:
            self.result = "loss"
            return self.get_state(), self.LOSS_REWARD, True
        if self.board.is_full():
            self.result = "draw"
            return self.get_state(), self.DRAW_REWARD, True
        return self.get_state(), self.MOVE_REWARD, False
    def get_result(self):
        return self.result

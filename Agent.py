
import random


class Agent:
    def legal_actions(self, state):
        return [i for i, c in enumerate(state) if c == "."]
    def choose_action(self, state):
        return random.choice(self.legal_actions(state))
    def update(self, state, action, reward, next_state, done):
        pass # learns nothing yet: Part 3

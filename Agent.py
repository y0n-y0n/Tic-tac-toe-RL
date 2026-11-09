
import random


class Agent:
    # def legal_actions(self, state):
    #     return [i for i, c in enumerate(state) if c == "."]
    # def choose_action(self, state):
    #     return random.choice(self.legal_actions(state))
    # def update(self, state, action, reward, next_state, done):
    #     pass # learns nothing yet: Part 3
    def __init__(self, alpha=0.15, gamma=0.9, epsilon=1.0, epsilon_decay=0.9999, min_epsilon=0.05):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)
    def legal_actions(self, state):
        return [i for i, c in enumerate(state) if c == "."]
    def best_action(self, state):
        legal_actions = self.legal_actions(state)
        if not legal_actions:
            return None
        q_values = [self.get_q_value(state, action) for action in legal_actions]
        max_q_value = max(q_values)
        best_actions = [action for action, q in zip(legal_actions, q_values) if q == max_q_value]
        return random.choice(best_actions)
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.legal_actions(state))
        else:
            return self.best_action(state)
    def update(self, state, action, reward, next_state, done):
        current_q = self.get_q_value(state, action)
        if done:
            target_q = reward
        else:
            next_best_action = self.best_action(next_state)
            next_q = self.get_q_value(next_state, next_best_action) if next_best_action is not None else 0.0
            target_q = reward + self.gamma * next_q
        new_q = current_q + self.alpha * (target_q - current_q)
        self.q_table[(state, action)] = new_q
    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
    def save_q_table(self, filename):
        import pickle
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
    def load_q_table(self, filename):
        import pickle
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)
        

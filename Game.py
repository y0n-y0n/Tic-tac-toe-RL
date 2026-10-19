from Environment import Environment
from Agent import Agent
import random

class Game:
    def __init__(self):
        self.agent: Agent
        self.env: Environment
        self.num_episodes = 100000
        self.report_every = 10000
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.total_wins = 0
        self.total_losses = 0
        self.total_draws = 0
        self.seen_states = set()

    def play_episode(self):
        state = self.env.reset(agent_starts=random.choice([True, False]))
        self.seen_states.add(state)
        done = False
        while not done:
            action = self.agent.choose_action(state)
            next_state, reward, done = self.env.step(action)
            self.seen_states.add(next_state)
            self.agent.update(state, action, reward, next_state, done)
            state = next_state
        return self.env.get_result()

    def record_results(self,results):
        for result in results:
            if result == "win":
                self.wins += 1
            elif result == "loss":
                self.losses += 1
            elif result == "draw":
                self.draws += 1
    def report_results(self):
        print(f"Total Wins: {self.total_wins}, Total Losses: {self.total_losses}, Total Draws: {self.total_draws}")
        print(f"Wins in last {self.report_every} episodes: {self.wins}, Losses: {self.losses}, Draws: {self.draws}")

    def train(self):
        self.agent = Agent()
        self.env = Environment()
        results = []
        for episode in range(1, self.num_episodes + 1):
            result = self.play_episode()
            results.append(result)
            if episode % self.report_every == 0:
                self.record_results(results)
                self.total_wins += self.wins
                self.total_losses += self.losses
                self.total_draws += self.draws
                self.report_results()
                results = []
                self.wins, self.losses, self.draws = 0, 0, 0
        print(f"Different states seen: {len(self.seen_states)}")
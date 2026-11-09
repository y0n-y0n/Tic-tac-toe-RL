from Game import Game
game = Game()
game.train()
# claude
game.agent.save_q_table("q_table.pkl")
print(f"Saved Q-table with {len(game.agent.q_table)} entries to q_table.pkl")

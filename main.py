from Game import Game
game = Game()
game.train()
print(game.report_results())
print(f"Different states seen: {len(game.seen_states)}")
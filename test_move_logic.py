# claude: whole file
import unittest
from board import Board
from Agent import Agent
from move_logic import play_move

E = "."


def make_agents():
    # Deterministic stand-ins so the tests don't depend on q_table.pkl
    return {"random": Agent(epsilon=1.0, min_epsilon=1.0),
            "qtable": Agent(epsilon=0.0, min_epsilon=0.0)}


class TestBoardLegality(unittest.TestCase):
    def legal(self, grid):
        b = Board()
        return b.load(grid) and b.is_legal()

    def test_empty_board_is_legal(self):
        self.assertTrue(self.legal([[E] * 3 for _ in range(3)]))

    def test_wrong_shape(self):
        self.assertFalse(self.legal([[E, E, E], [E, E, E]]))
        self.assertFalse(self.legal([[E, E], [E, E, E], [E, E, E]]))
        self.assertFalse(self.legal("X........"))

    def test_bad_cell_value(self):
        self.assertFalse(self.legal([["Z", E, E], [E, E, E], [E, E, E]]))

    def test_piece_count_difference(self):
        self.assertFalse(self.legal([["X", "X", E], [E, E, E], [E, E, E]]))
        self.assertTrue(self.legal([["X", E, E], [E, E, E], [E, E, E]]))
        self.assertTrue(self.legal([["O", E, E], [E, E, E], [E, E, E]]))

    def test_both_players_won(self):
        self.assertFalse(self.legal([["X", "X", "X"], ["O", "O", "O"], [E, E, E]]))

    def test_winning_line(self):
        b = Board()
        b.load([["X", "O", "O"], [E, "X", E], ["O", E, "X"]])
        self.assertEqual(b.winning_line(), [0, 4, 8])


class TestPlayMove(unittest.TestCase):
    def setUp(self):
        self.agents = make_agents()

    def test_missing_field(self):
        resp, code = play_move({"agent": "random"}, self.agents)
        self.assertEqual(code, 400)
        self.assertIn("board", resp["error"])

    def test_unknown_agent(self):
        resp, code = play_move({"board": [[E] * 3] * 3, "agent": "smart"}, self.agents)
        self.assertEqual((resp, code), ({"error": "Unknown agent: 'smart'"}, 400))

    def test_invalid_board(self):
        resp, code = play_move({"board": [["X", "X", E], [E] * 3, [E] * 3], "agent": "random"}, self.agents)
        self.assertEqual(code, 400)

    def test_not_a_json_object(self):
        _, code = play_move(None, self.agents)
        self.assertEqual(code, 400)

    def test_agent_starts_on_empty_board(self):
        resp, code = play_move({"board": [[E] * 3 for _ in range(3)], "agent": "random"}, self.agents)
        self.assertEqual(code, 200)
        self.assertEqual(resp["status"], "playing")
        r, c = divmod(resp["agent_move"], 3)
        self.assertEqual(resp["board"][r][c], "O")

    def test_agent_never_plays_occupied_square(self):
        grid = [["X", "O", "X"], ["X", "O", E], ["O", "X", E]]
        for _ in range(50):
            resp, _ = play_move({"board": grid, "agent": "random"}, self.agents)
            self.assertIn(resp["agent_move"], (5, 8))

    def test_agent_wins(self):
        # Only square 7 is empty, and playing it completes O's middle column
        grid = [["X", "O", "X"], ["X", "O", "O"], ["O", E, "X"]]
        resp, code = play_move({"board": grid, "agent": "qtable"}, self.agents)
        self.assertEqual(code, 200)
        self.assertEqual(resp["agent_move"], 7)
        self.assertEqual(resp["status"], "agent_wins")
        self.assertEqual(resp["winning_line"], [1, 4, 7])

    def test_human_already_won(self):
        grid = [["X", "X", "X"], ["O", "O", E], [E, E, E]]
        resp, code = play_move({"board": grid, "agent": "qtable"}, self.agents)
        self.assertEqual(code, 200)
        self.assertIsNone(resp["agent_move"])
        self.assertEqual(resp["status"], "human_wins")
        self.assertEqual(resp["winning_line"], [0, 1, 2])
        self.assertEqual(resp["board"], grid)

    def test_board_full_is_draw(self):
        grid = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        resp, _ = play_move({"board": grid, "agent": "qtable"}, self.agents)
        self.assertIsNone(resp["agent_move"])
        self.assertEqual(resp["status"], "draw")
        self.assertIsNone(resp["winning_line"])

    def test_agent_last_move_draws(self):
        grid = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", E]]
        resp, _ = play_move({"board": grid, "agent": "qtable"}, self.agents)
        self.assertEqual(resp["agent_move"], 8)
        self.assertEqual(resp["status"], "draw")


if __name__ == "__main__":
    unittest.main()

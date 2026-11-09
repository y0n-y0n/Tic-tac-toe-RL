# claude: whole file
from board import Board
from Agent import Agent

AGENT_MARK = "O"
HUMAN_MARK = "X"
Q_TABLE_FILE = "q_table.pkl"


def load_agents(q_table_file=Q_TABLE_FILE):
    """Build the playable agents. Both use the Agent class:
    random  -> epsilon 1, always a random legal move
    qtable  -> epsilon 0, always the best move from the trained Q-table"""
    qtable = Agent(epsilon=0.0, min_epsilon=0.0)
    qtable.load_q_table(q_table_file)
    random_agent = Agent(epsilon=1.0, min_epsilon=1.0)
    return {"qtable": qtable, "random": random_agent}


def game_status(board):
    """Status string for the board as it is now."""
    winner = board.winner()
    if winner == AGENT_MARK:
        return "agent_wins"
    if winner == HUMAN_MARK:
        return "human_wins"
    if board.is_full():
        return "draw"
    return "playing"


def play_move(request_data, agents):
    """Handle one /api/move request.
    Returns (response_dict, http_status_code)."""
    if not isinstance(request_data, dict):
        return {"error": "Request body must be a JSON object"}, 400
    for field in ("board", "agent"):
        if field not in request_data:
            return {"error": f"Missing field: '{field}'"}, 400

    agent_name = request_data["agent"]
    if agent_name not in agents:
        return {"error": f"Unknown agent: '{agent_name}'"}, 400

    board = Board()
    if not board.load(request_data["board"]) or not board.is_legal():
        return {"error": "Invalid board"}, 400

    agent_move = None
    if game_status(board) == "playing":
        agent_move = agents[agent_name].choose_action(board.to_key())
        board.make_move(divmod(agent_move, 3), AGENT_MARK)

    return {
        "board": board.grid,
        "agent_move": agent_move,
        "status": game_status(board),
        "winning_line": board.winning_line(),
    }, 200

# claude: whole file
import os
from flask import Flask, request, jsonify, render_template
from move_logic import load_agents, play_move, Q_TABLE_FILE

app = Flask(__name__)

# Load the trained Q-table once, on startup
q_table_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), Q_TABLE_FILE)
if not os.path.exists(q_table_path):
    raise SystemExit(f"{Q_TABLE_FILE} not found - run main.py to train the agent first")
agents = load_agents(q_table_path)


@app.route("/")
def tic_tac_toe():
    return render_template("index.html")


@app.route("/api/move", methods=["POST"])
def move():
    data = request.get_json(silent=True)
    response, status_code = play_move(data, agents)
    return jsonify(response), status_code


if __name__ == "__main__":
    app.run(debug=True)

<!-- claude: whole file -->
# Tic tac toe – Software Specification

## Contract

### `POST /api/move`

Send the board after the human moves. When the agent starts, send an empty board.

**Request**

```json
{"board": [["X", "O", "."], [".", "O", "."], [".", ".", "X"]], "agent": "qtable"}
```

- `board`: a JSON array of 3 rows, each an array of 3 strings.
  `"O"` = agent, `"X"` = human, `"."` = empty.
  The first row is the top row; index 0 in each row is that row's left square.
  Square indexes 0-8 run left to right, top to bottom (index = row * 3 + col).
- `agent`: `"qtable"` (the Q-learning agent; `"random"` is also accepted by the API).

**Success, status 200**

```json
{"board": [["X", "O", "."], [".", "O", "."], [".", "O", "X"]],
 "agent_move": 7, "status": "agent_wins", "winning_line": [1, 4, 7]}
```

- `board`: the board after the agent's move, same 3x3 format as the request.
- `status`: `"playing"` | `"agent_wins"` | `"human_wins"` | `"draw"`
- `agent_move`: 0-8, or `null` if the game was already over when the board arrived
  (the human's move won or filled the board).
- `winning_line`: `null`, or the 3 square indexes of the winning line, e.g. `[2, 4, 6]`.
  Set for both agent and human wins.

**Error, status 400**

```json
{"error": "Unknown agent: 'smart'"}
```

Returned for a missing field, an unknown agent, or an invalid board.
Board legality is decided by the `Board` class: wrong shape, a cell that is not
`"X"`/`"O"`/`"."`, piece counts differing by more than 1, or both players having
a line are all invalid.

## Behavior

- Main page: a 3x3 board, the page title "Tic tac toe" above it, and a status bar below it.
- Status bar text: `""` (before the first game starts) / "Your turn" / "Agent turn" /
  "You win!" / "You lose!" / "Draw!" / an error message if a request fails.
- On a win, the three squares of `winning_line` are highlighted.
- Human is always X (red cross), agent is always O (blue ring), regardless of who starts.
- Three controls, in a column to the left of the board:
  - **New game** – a button that resets the board and starts a new game with the
    current settings.
  - **Who starts** – a toggle between "You start" and "Agent starts".
  - **Choose agent** – a drop-down menu of agents. Currently hard-coded to
    "Q-learning" only.
- Changing "Who starts" or "Choose agent" mid-game only affects the next game.

## Q-learning agent

- Trained with the current parameters in `Game.py` / `Agent.py`.
- The trained Q-table is saved as a file in this project and loaded by the server on startup.
- When playing, the agent uses ε = 0 (always picks its best known move).

## Tech

- Backend: Flask, serving both the API and the page.
- Frontend: HTML, CSS and JS kept in separate, organised files.

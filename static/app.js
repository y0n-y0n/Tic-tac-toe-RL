//claude: whole file

// ---------- Constants ----------
const HUMAN = "X";
const AGENT = "O";
const EMPTY = ".";
//claude
const AGENT_DELAY_MS = 600; // pause before the agent plays, so its move is easy to follow

const STATUS_TEXT = {
    playing: "Your turn",
    agent_wins: "You lose!",
    human_wins: "You win!",
    draw: "Draw!",
};

// Red cross with a black outline, and a blue ring (as in the UI mockup)
const MARK_SVG = {
    X: `<svg viewBox="0 0 100 100" aria-hidden="true">
            <path d="M30 10 L50 30 L70 10 L90 30 L70 50 L90 70 L70 90 L50 70 L30 90 L10 70 L30 50 L10 30 Z"
                  fill="#ff0000" stroke="#000" stroke-width="2" stroke-linejoin="round"/>
        </svg>`,
    O: `<svg viewBox="0 0 100 100" aria-hidden="true">
            <circle cx="50" cy="50" r="37" fill="none" stroke="#4a86e8" stroke-width="22"/>
            <circle cx="50" cy="50" r="48" fill="none" stroke="#555" stroke-width="1"/>
            <circle cx="50" cy="50" r="26" fill="none" stroke="#555" stroke-width="1"/>
        </svg>`,
};

// ---------- Elements ----------
const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status");
const newGameBtn = document.getElementById("new-game");
const whoStartsBtn = document.getElementById("who-starts");
const whoStartsValue = document.getElementById("who-starts-value");
const agentSelect = document.getElementById("agent-select");

// ---------- State ----------
// Settings: what the controls currently say (used when the next game starts)
const settings = { humanStarts: true };

// The game in progress. Settings are copied in at "New game", so changing
// a control mid-game only affects the next game.
let game = null; // { id, board, agent, humanTurn, over, winningLine }
let gameCounter = 0; // lets us ignore replies that belong to an old game

function emptyBoard() {
    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ];
}

// ---------- Rendering ----------
function createCells() {
    for (let i = 0; i < 9; i++) {
        const cell = document.createElement("button");
        cell.className = "cell";
        cell.dataset.index = i;
        cell.addEventListener("click", () => onCellClick(i));
        boardEl.appendChild(cell);
    }
}

function render() {
    const cells = boardEl.children;
    for (let i = 0; i < 9; i++) {
        const row = Math.floor(i / 3);
        const col = i % 3;
        const mark = game ? game.board[row][col] : EMPTY;
        const cell = cells[i];

        cell.innerHTML = mark === EMPTY ? "" : MARK_SVG[mark];
        cell.disabled = !game || game.over || !game.humanTurn || mark !== EMPTY;
        cell.classList.toggle("win", !!(game && game.winningLine && game.winningLine.includes(i)));

        const who = mark === HUMAN ? "X (you)" : mark === AGENT ? "O (agent)" : "empty";
        cell.setAttribute("aria-label", `Row ${row + 1}, column ${col + 1}: ${who}`);
    }
}

function setStatus(text, isError = false) {
    statusEl.textContent = text;
    statusEl.classList.toggle("error", isError);
}

// ---------- Server ----------
// undoBoard: the board to go back to if the request fails
// (null when the agent opens the game - then there is nothing to undo)
async function requestAgentMove(undoBoard) {
    const id = game.id;
    game.humanTurn = false;
    setStatus("Agent turn");
    render();

    //claude
    await new Promise(resolve => setTimeout(resolve, AGENT_DELAY_MS));
    if (id !== game.id) return; // "New game" was pressed during the pause

    try {
        const response = await fetch("/api/move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ board: game.board, agent: game.agent }),
        });
        const data = await response.json();
        if (id !== game.id) return; // "New game" was pressed while waiting

        if (!response.ok) {
            throw new Error(data.error || `Server error ${response.status}`);
        }

        game.board = data.board;
        game.winningLine = data.winning_line;
        game.over = data.status !== "playing";
        game.humanTurn = !game.over;
        setStatus(STATUS_TEXT[data.status]);
    } catch (err) {
        if (id !== game.id) return;
        if (undoBoard) {
            // Undo the human's last move so they can try again
            game.board = undoBoard;
            game.humanTurn = true;
            setStatus(`Error: ${err.message} - try again`, true);
        } else {
            // The agent's opening move failed: the game can't continue
            game.over = true;
            setStatus(`Error: ${err.message} - press New game to retry`, true);
        }
    }
    render();
}

// ---------- Events ----------
function onCellClick(index) {
    if (!game || game.over || !game.humanTurn) return;
    const row = Math.floor(index / 3);
    const col = index % 3;
    if (game.board[row][col] !== EMPTY) return;

    const boardBefore = game.board.map(r => [...r]);
    game.board[row][col] = HUMAN;
    requestAgentMove(boardBefore);
}

function startNewGame() {
    gameCounter++;
    game = {
        id: gameCounter,
        board: emptyBoard(),
        agent: agentSelect.value,
        humanTurn: settings.humanStarts,
        over: false,
        winningLine: null,
    };

    if (settings.humanStarts) {
        setStatus("Your turn");
        render();
    } else {
        requestAgentMove(null);
    }
}

function toggleWhoStarts() {
    settings.humanStarts = !settings.humanStarts;
    whoStartsValue.textContent = settings.humanStarts ? "You start" : "Agent starts";
}

// ---------- Start ----------
newGameBtn.addEventListener("click", startNewGame);
whoStartsBtn.addEventListener("click", toggleWhoStarts);
createCells();
render(); // empty, disabled board and "" status until "New game" is pressed

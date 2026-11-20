# Project Report: XO (Tic-Tac-Toe) with Minimax & Alpha-Beta Pruning

**Course:** Introduction to Artificial Intelligence (CAI3101 & CS366)
**Team members:** (write the 6 names here)

## 1. Game chosen
XO (Tic-Tac-Toe), 3x3 board. The human plays **X**, the computer plays **O**. Python backend + web interface (HTML/JS in the browser).

## 2. How to run
1. Install Python 3.8+ (no extra libraries needed).
2. In the project folder run: `python server.py`
3. The browser opens at `http://localhost:8000` (or open it manually).
4. Optional: `python test_ai.py` (tests) and `python benchmark.py` (Minimax vs Alpha-Beta).

## 3. How the program works
| File | Job |
|---|---|
| `game.py` | Game logic: board, legal moves, win check (8 lines), draw check, make move |
| `ai.py` | Minimax, Alpha-Beta, node counter, evaluation, levels |
| `server.py` | Small web server (Python standard library). One endpoint `/api/play` receives the board + human move + settings, returns the new board, game status and the AI move info (cell, nodes, time) |
| `static/index.html` | The interface: choose who plays first, algorithm and level; click a cell to play; Hint button; shows turn, last AI move, winner/draw, winning line highlight, New Game button |
| `test_ai.py`, `benchmark.py` | Testing and measurements |

Flow: the player clicks a cell -> the browser sends the board to Python -> Python places X, checks the game, runs the AI to place O, checks again -> the browser draws the result.

## 4. How the algorithms work
The board is a tree: each node is a position, each edge is a move. O is the **MAX** player and X is the **MIN** player.

**Terminal scores:** O wins = `100 - depth`, X wins = `depth - 100`, draw = `0`. Using depth makes the computer prefer a faster win and a slower loss.

**Minimax:** visits all children, MAX takes the highest value and MIN takes the lowest. Every visited position increases the node counter.

**Alpha-Beta Pruning:** same search, but keeps `alpha` (best value MAX can already guarantee) and `beta` (best value MIN can already guarantee). When `alpha >= beta`, the remaining children cannot change the result, so they are skipped (pruned). It returns **the same move** as Minimax with fewer nodes. At the root, the first best move is kept (strict `>`), so both algorithms always agree.

**Levels:**
- **Easy:** random empty cell (no search).
- **Medium:** Minimax/Alpha-Beta with depth limit 2. When the limit stops the search at a non-final position, a simple evaluation is used: for every line that is still open for one player, add +1/+2 for O (1 or 2 marks) and -1/-2 for X.
- **Hard:** search to the end of the game (no depth limit). The computer never loses.

**Hint button:** the same Alpha-Beta search is run from the human's point of view (X is the MIN player, so it takes the lowest value) with no depth limit. The interface highlights the best cell and explains it: "wins the game", "blocks the computer's winning move" or "best move by full search", and tells the player the result with best play (win / draw / difficult). Endpoint: `/api/hint`.

## 5. Results
`test_ai.py` checks:
- Minimax and Alpha-Beta choose the same move in all 4,520 reachable positions (Medium and Hard).
- Hard was played against **every possible human strategy**, both when the human starts and when the computer starts: **0 computer losses** (457 computer wins, 185 draws).
- A human who always follows the Hint never loses against Hard, and always takes an immediate win when one exists.

`benchmark.py` (nodes visited by the computer):

| Position | Level | Minimax | Alpha-Beta |
|---|---|---:|---:|
| Empty board (computer first) | Hard | 549,946 | 20,866 |
| X in corner | Hard | 59,705 | 2,788 |
| X in centre | Hard | 55,505 | 2,459 |
| X in corner | Medium | 65 | 36 |

Alpha-Beta visits about **20-26x fewer nodes** on Hard (e.g. 549,946 -> 20,866 on the empty board) with the same best move.

## 6. Work distribution
| Member | Task |
|---|---|
| 1 | Game logic (`game.py`) |
| 2 | Minimax (`ai.py`) |
| 3 | Alpha-Beta (`ai.py`) |
| 4 | Evaluation function and levels |
| 5 | Web interface (`index.html`) and server (`server.py`) |
| 6 | Testing, benchmark and report |

(Edit this table to match what each member really did.)

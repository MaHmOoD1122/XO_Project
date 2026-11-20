"""Minimax and Alpha-Beta Pruning for XO. Computer = 'O' (MAX), human = 'X' (MIN).
Both algorithms count the nodes they visit and pick the SAME move."""
import random
import time
from game import EMPTY, LINES, legal_moves, get_winner, is_full, make_move

COMPUTER, HUMAN = "O", "X"
WIN = 100
LEVEL_DEPTH = {"easy": None, "medium": 2, "hard": None}   # hard = no limit


class Stats:
    def __init__(self):
        self.nodes = 0


def evaluate(board):
    """Heuristic used only when the depth limit stops the search (Medium).
    +1/+2 for each line still open for O (with 1/2 O marks), -1/-2 for X."""
    score = 0
    for line in LINES:
        cells = [board[i] for i in line]
        if "X" not in cells and "O" in cells:
            score += cells.count("O")
        elif "O" not in cells and "X" in cells:
            score -= cells.count("X")
    return score


def terminal_value(board, depth):
    """Return a score if the game is over, else None. Faster wins score higher."""
    winner, _ = get_winner(board)
    if winner == COMPUTER:
        return WIN - depth
    if winner == HUMAN:
        return depth - WIN
    if is_full(board):
        return 0
    return None


def minimax(board, player, depth, limit, stats):
    stats.nodes += 1
    t = terminal_value(board, depth)
    if t is not None:
        return t
    if limit is not None and depth >= limit:
        return evaluate(board)
    if player == COMPUTER:
        best = -10**9
        for m in legal_moves(board):
            best = max(best, minimax(make_move(board, m, player), HUMAN, depth + 1, limit, stats))
        return best
    best = 10**9
    for m in legal_moves(board):
        best = min(best, minimax(make_move(board, m, player), COMPUTER, depth + 1, limit, stats))
    return best


def alphabeta(board, player, depth, limit, alpha, beta, stats):
    stats.nodes += 1
    t = terminal_value(board, depth)
    if t is not None:
        return t
    if limit is not None and depth >= limit:
        return evaluate(board)
    if player == COMPUTER:
        best = -10**9
        for m in legal_moves(board):
            best = max(best, alphabeta(make_move(board, m, player), HUMAN, depth + 1, limit, alpha, beta, stats))
            alpha = max(alpha, best)
            if alpha >= beta:        # prune
                break
        return best
    best = 10**9
    for m in legal_moves(board):
        best = min(best, alphabeta(make_move(board, m, player), COMPUTER, depth + 1, limit, alpha, beta, stats))
        beta = min(beta, best)
        if alpha >= beta:            # prune
            break
    return best


def best_move(board, algorithm="alphabeta", limit=None):
    """Return (move, nodes_visited) for the computer (O)."""
    stats = Stats()
    stats.nodes += 1                 # the root node
    best_val, best_m = -10**9, None
    for m in legal_moves(board):
        child = make_move(board, m, COMPUTER)
        if algorithm == "minimax":
            v = minimax(child, HUMAN, 1, limit, stats)
        else:
            v = alphabeta(child, HUMAN, 1, limit, best_val, 10**9, stats)
        if v > best_val:             # strict > keeps the first best move (same for both algorithms)
            best_val, best_m = v, m
    return best_m, stats.nodes


def ai_move(board, level="hard", algorithm="alphabeta"):
    """Pick the computer's move according to the level. Returns a dict."""
    t0 = time.perf_counter()
    if level == "easy":
        move, nodes = random.choice(legal_moves(board)), 0
    else:
        move, nodes = best_move(board, algorithm, LEVEL_DEPTH[level])
    return {"cell": move, "nodes": nodes,
            "time_ms": round((time.perf_counter() - t0) * 1000, 2)}


def hint_move(board):
    """Best move for the HUMAN (X = MIN player), full search with Alpha-Beta.
    Returns the cell, a short reason and what the result will be with best play."""
    stats = Stats()
    best_val, best_m = 10**9, None
    for m in legal_moves(board):
        child = make_move(board, m, HUMAN)
        v = alphabeta(child, COMPUTER, 1, None, -10**9, best_val, stats)
        if v < best_val:                       # X wants the LOWEST value
            best_val, best_m = v, m
    if get_winner(make_move(board, best_m, HUMAN))[0] == HUMAN:
        reason = "This move wins the game!"
    elif get_winner(make_move(board, best_m, COMPUTER))[0] == COMPUTER:
        reason = "Blocks the computer's winning move."
    else:
        reason = "Best move found by full search."
    outcome = "win" if best_val < 0 else "loss" if best_val > 0 else "draw"
    return {"cell": best_m, "reason": reason, "outcome": outcome, "nodes": stats.nodes}

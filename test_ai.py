"""Run:  python test_ai.py"""
from game import new_board, legal_moves, make_move, game_status
from ai import best_move, ai_move, hint_move, LEVEL_DEPTH


def all_positions_agree():
    """Minimax and Alpha-Beta must choose the same move in every reachable position (O to move)."""
    seen, checked = set(), 0
    def walk(board, player):
        nonlocal checked
        key = (tuple(board), player)
        if key in seen or game_status(board)["over"]:
            return
        seen.add(key)
        if player == "O":
            for limit in (None, 2):
                m1, n1 = best_move(board, "minimax", limit)
                m2, n2 = best_move(board, "alphabeta", limit)
                assert m1 == m2, (board, limit, m1, m2)
                assert n2 <= n1
            checked += 1
        for m in legal_moves(board):
            walk(make_move(board, m, player), "O" if player == "X" else "X")
    walk(new_board(), "X"); walk(new_board(), "O")
    return checked


def hard_never_loses():
    """Try EVERY possible human strategy against Hard (both starting players)."""
    results = {"O": 0, "X": 0, "draw": 0}
    def play(board, turn, first_is_human):
        st = game_status(board)
        if st["over"]:
            results[st["winner"] or "draw"] += 1
            return
        if turn == "X":
            for m in legal_moves(board):
                play(make_move(board, m, "X"), "O", first_is_human)
        else:
            m = ai_move(board, "hard", "alphabeta")["cell"]
            play(make_move(board, m, "O"), "X", first_is_human)
    play(new_board(), "X", True)    # human first
    play(new_board(), "O", False)   # computer first
    return results


def hint_never_loses():
    """A human who ALWAYS follows the hint must never lose against Hard (both starters),
    and must take an immediate win when one exists."""
    results = {"O": 0, "X": 0, "draw": 0}
    def play(board, turn):
        st = game_status(board)
        if st["over"]:
            results[st["winner"] or "draw"] += 1
            return
        if turn == "X":
            h = hint_move(board)
            if any(game_status(make_move(board, m, "X"))["winner"] == "X" for m in legal_moves(board)):
                assert game_status(make_move(board, h["cell"], "X"))["winner"] == "X"
            play(make_move(board, h["cell"], "X"), "O")
        else:
            play(make_move(board, ai_move(board, "hard", "alphabeta")["cell"], "O"), "X")
    play(new_board(), "X"); play(new_board(), "O")
    return results


if __name__ == "__main__":
    print("Positions where Minimax == Alpha-Beta:", all_positions_agree())
    r = hard_never_loses()
    print("Hard vs every human strategy ->", r)
    assert r["X"] == 0, "Hard AI lost a game!"
    h = hint_never_loses()
    print("Following the hint vs Hard ->", h)
    assert h["O"] == 0, "Hint led to a loss!"
    print("ALL TESTS PASSED")

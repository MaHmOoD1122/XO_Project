"""Game logic for XO (Tic-Tac-Toe). Board = list of 9 cells: ' ', 'X' or 'O'.
Cells are numbered 0..8, left-to-right, top-to-bottom."""

EMPTY = " "
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8),      # rows
         (0, 3, 6), (1, 4, 7), (2, 5, 8),      # columns
         (0, 4, 8), (2, 4, 6)]                 # diagonals


def new_board():
    return [EMPTY] * 9


def legal_moves(board):
    return [i for i, c in enumerate(board) if c == EMPTY]


def get_winner(board):
    """Return (symbol, winning_line) or (None, None)."""
    for a, b, c in LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a], [a, b, c]
    return None, None


def is_full(board):
    return EMPTY not in board


def game_status(board):
    winner, line = get_winner(board)
    draw = winner is None and is_full(board)
    return {"over": winner is not None or draw,
            "winner": winner, "line": line, "draw": draw}


def make_move(board, cell, player):
    """Return a NEW board with `player` placed at `cell`."""
    if not (0 <= cell < 9) or board[cell] != EMPTY:
        raise ValueError("illegal move")
    nb = list(board)
    nb[cell] = player
    return nb

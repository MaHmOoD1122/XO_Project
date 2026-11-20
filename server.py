"""Tiny web server (Python standard library only - nothing to install).
Run:  python server.py   then open http://localhost:8000"""
import json
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from game import legal_moves, make_move, game_status
from ai import ai_move, hint_move

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8000


def handle_play(data):
    board = data["board"]
    if not (isinstance(board, list) and len(board) == 9 and all(c in (" ", "X", "O") for c in board)):
        raise ValueError("bad board")
    level = data.get("level", "hard")
    algorithm = data.get("algorithm", "alphabeta")
    if level not in ("easy", "medium", "hard") or algorithm not in ("minimax", "alphabeta"):
        raise ValueError("bad settings")

    if game_status(board)["over"]:
        raise ValueError("game is over")

    move = data.get("move")
    if move is not None:                      # human plays X
        board = make_move(board, int(move), "X")

    ai = None
    status = game_status(board)
    if not status["over"] and legal_moves(board):   # computer plays O
        ai = ai_move(board, level, algorithm)
        board = make_move(board, ai["cell"], "O")
        status = game_status(board)
    return {"board": board, "status": status, "ai": ai}


def handle_hint(data):
    board = data["board"]
    if not (isinstance(board, list) and len(board) == 9 and all(c in (" ", "X", "O") for c in board)):
        raise ValueError("bad board")
    if game_status(board)["over"]:
        raise ValueError("game is over")
    return hint_move(board)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open(os.path.join(HERE, "static", "index.html"), "rb") as f:
                self._send(200, f.read(), "text/html; charset=utf-8")
        else:
            self._send(404, b"Not found", "text/plain")

    def do_POST(self):
        if self.path not in ("/api/play", "/api/hint"):
            return self._send(404, b"Not found", "text/plain")
        try:
            length = int(self.headers.get("Content-Length", 0))
            handler = handle_play if self.path == "/api/play" else handle_hint
            result = handler(json.loads(self.rfile.read(length)))
            self._send(200, json.dumps(result).encode(), "application/json")
        except (ValueError, KeyError, TypeError) as e:
            self._send(400, json.dumps({"error": str(e)}).encode(), "application/json")

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"XO game running at http://localhost:{PORT}  (Ctrl+C to stop)")
    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except Exception:
        pass
    server.serve_forever()

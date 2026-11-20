"""Compare nodes visited by Minimax and Alpha-Beta. Run: python benchmark.py"""
import time
from game import new_board, make_move
from ai import best_move

positions = {
    "Empty board (computer first)": new_board(),
    "After X in corner (cell 0)": make_move(new_board(), 0, "X"),
    "After X in centre (cell 4)": make_move(new_board(), 4, "X"),
}
print(f"{'Position':32}{'Level':8}{'Algorithm':11}{'Nodes':>10}{'Time(ms)':>10}")
for name, b in positions.items():
    for level, lim in (("Medium", 2), ("Hard", None)):
        for algo in ("minimax", "alphabeta"):
            t = time.perf_counter(); m, n = best_move(b, algo, lim)
            print(f"{name:32}{level:8}{algo:11}{n:>10,}{(time.perf_counter()-t)*1000:>10.1f}")

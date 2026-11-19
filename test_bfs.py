from game.board import Board
from algorithms.bfs import bfs

board = Board()

start = board.thief_start
goal = board.key_pos

path, visited = bfs(
    board,
    start,
    goal,
    return_visited=True
)

print("Path:", path)
print("Visited nodes:", visited)
print("Path length:", len(path))
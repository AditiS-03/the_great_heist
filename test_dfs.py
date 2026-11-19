
from game.board import Board
from algorithms.dfs import dfs

board = Board()

start = board.thief_start
goal = board.key_pos

path, visited = dfs(
    board,
    start,
    goal,
    return_visited=True
)

print("DFS Path:", path)
print("Visited Nodes:", visited)
print("Path Length:", len(path))

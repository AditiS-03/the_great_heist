
from collections import deque


def bfs(board, start, goal, vault_unlocked=False, return_visited=False):

    queue = deque([start])

    parent = {
        start: None
    }

    visited = []

    while queue:

        current = queue.popleft()

        visited.append(current)

        # Check whether goal is reached
        if current == goal:
            break

        # Explore neighboring cells
        for neighbor in board.neighbors(
            current,
            vault_unlocked
        ):

            if neighbor not in parent:

                parent[neighbor] = current

                queue.append(neighbor)

    # Reconstruct the path
    path = []

    if goal in parent:

        current = goal

        while current is not None:

            path.append(current)

            current = parent[current]

        path.reverse()

    # Return path and explored nodes if requested
    if return_visited:

        return path, visited

    return path


def dfs(board, start, goal, vault_unlocked=False, return_visited=False):

    stack = [start]

    parent = {
        start: None
    }

    visited = []
    explored = set()

    while stack:

        current = stack.pop()

        if current in explored:
            continue

        explored.add(current)
        visited.append(current)

        # Check whether goal is reached
        if current == goal:
            break

        # Explore neighboring cells
        neighbors = list(
            board.neighbors(current, vault_unlocked)
        )

        for neighbor in neighbors:

            if neighbor not in parent:

                parent[neighbor] = current

                stack.append(neighbor)

    # Reconstruct path
    path = []

    if goal in parent:

        current = goal

        while current is not None:

            path.append(current)

            current = parent[current]

        path.reverse()

    if return_visited:

        return path, visited

    return path

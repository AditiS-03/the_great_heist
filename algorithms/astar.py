
import heapq

from algorithms.heuristics import manhattan


def astar(
    board,
    start,
    goal,
    vault_unlocked=False,
    return_visited=False
):

    # Priority queue: (f_score, g_score, position)
    priority_queue = []

    heapq.heappush(
        priority_queue,
        (manhattan(start, goal), 0, start)
    )

    parent = {
        start: None
    }

    cost = {
        start: 0
    }

    visited = []

    while priority_queue:

        f_score, g_score, current = heapq.heappop(
            priority_queue
        )

        if current in visited:
            continue

        visited.append(current)

        # Goal reached
        if current == goal:
            break

        # Explore neighboring positions
        for neighbor in board.neighbors(
            current,
            vault_unlocked
        ):

            new_cost = g_score + 1

            if new_cost < cost.get(
                neighbor,
                float("inf")
            ):

                cost[neighbor] = new_cost

                parent[neighbor] = current

                heuristic = manhattan(
                    neighbor,
                    goal
                )

                total_cost = new_cost + heuristic

                heapq.heappush(
                    priority_queue,
                    (
                        total_cost,
                        new_cost,
                        neighbor
                    )
                )

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


import random
from collections import deque


def get_neighbors(pos, cols, rows):
    x, y = pos

    candidates = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)
    ]

    return [
        p for p in candidates
        if 1 <= p[0] < cols - 1
        and 1 <= p[1] < rows - 1
    ]


def get_connected_cells(grid, start, blocked=None):
    rows = len(grid)
    cols = len(grid[0])

    queue = deque([start])
    visited = {start}

    while queue:
        current = queue.popleft()

        for neighbor in get_neighbors(
            current, cols, rows
        ):
            x, y = neighbor

            if neighbor in visited:
                continue

            if neighbor == blocked:
                continue

            if grid[y][x] == "W":
                continue

            visited.add(neighbor)
            queue.append(neighbor)

    return visited


def is_connected(grid, cells):
    if not cells:
        return False

    connected = get_connected_cells(
        grid,
        next(iter(cells))
    )

    return connected == cells


def generate_map(cols=15, rows=11, seed=None):

    rng = random.Random(seed)

    if cols < 7 or rows < 7:
        raise ValueError(
            "Map dimensions must be at least 7x7."
        )

    # --------------------------------
    # GENERATE RANDOM MUSEUM LAYOUT
    # --------------------------------

    grid = None
    floor_cells = None

    for attempt in range(150):

        candidate = [
            ["W" for _ in range(cols)]
            for _ in range(rows)
        ]

        # Create the walkable interior.
        for y in range(1, rows - 1):
            for x in range(1, cols - 1):

                if rng.random() < 0.16:
                    candidate[y][x] = "W"
                else:
                    candidate[y][x] = "."

        # Ensure that all walkable rooms and corridors
        # are connected.
        floors = {
            (x, y)
            for y in range(1, rows - 1)
            for x in range(1, cols - 1)
            if candidate[y][x] == "."
        }

        if len(floors) < 6:
            continue

        if is_connected(candidate, floors):
            grid = candidate
            floor_cells = floors
            break

    # Fallback: an open museum if random generation fails.
    if grid is None:

        grid = [
            ["W" for _ in range(cols)]
            for _ in range(rows)
        ]

        for y in range(1, rows - 1):
            for x in range(1, cols - 1):
                grid[y][x] = "."

        floor_cells = {
            (x, y)
            for y in range(1, rows - 1)
            for x in range(1, cols - 1)
        }

    # --------------------------------
    # SELECT A VALID LOCKED VAULT TILE
    # --------------------------------

    # The vault door must be removable without
    # disconnecting the remaining museum.
    vault_candidates = []

    for pos in floor_cells:

        connected_without_door = get_connected_cells(
            grid,
            next(iter(floor_cells - {pos})),
            blocked=pos
        )

        remaining = floor_cells - {pos}

        if connected_without_door == remaining:
            vault_candidates.append(pos)

    if not vault_candidates:
        # Open layouts always have suitable candidates.
        # This fallback removes some walls if necessary.
        for y in range(1, rows - 1):
            for x in range(1, cols - 1):
                grid[y][x] = "."

        floor_cells = {
            (x, y)
            for y in range(1, rows - 1)
            for x in range(1, cols - 1)
        }

        vault_candidates = list(floor_cells)

    vault_pos = rng.choice(vault_candidates)

    # --------------------------------
    # PLACE OBJECTS AND PLAYERS
    # --------------------------------

    available = list(floor_cells - {vault_pos})
    rng.shuffle(available)

    thief_start = available.pop()
    guard_start = available.pop()
    key_pos = available.pop()
    artifact_pos = available.pop()
    exit_pos = available.pop()

    # Mark the vault as a locked door.
    vx, vy = vault_pos
    grid[vy][vx] = "D"

    return {
        "grid": ["".join(row) for row in grid],
        "thief_start": thief_start,
        "guard_start": guard_start,
        "key_pos": key_pos,
        "vault_pos": vault_pos,
        "artifact_pos": artifact_pos,
        "exit_pos": exit_pos
    }

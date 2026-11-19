
from config import GRID_COLS, GRID_ROWS

DEFAULT_MAP = [
    "WWWWWWWWWWWWWWW",
    "W....W........W",
    "W....W..W.D...W",
    "W.......W.....W",
    "W.WWW...W..W..W",
    "W.............W",
    "W..W....W.....W",
    "W..W..........W",
    "W......W..W...W",
    "W.............W",
    "WWWWWWWWWWWWWWW"
]

class Board:

    def __init__(self, use_generated=False, seed=None):

        if use_generated:

            from constraints.map_generator import generate_map

            data = generate_map(
                cols=GRID_COLS,
                rows=GRID_ROWS,
                seed=seed
            )

            self.grid = [
                list(row) for row in data["grid"]
            ]

            self.thief_start = data["thief_start"]
            self.guard_start = data["guard_start"]
            self.key_pos = data["key_pos"]
            self.vault_pos = data["vault_pos"]
            self.artifact_pos = data["artifact_pos"]
            self.exit_pos = data["exit_pos"]

        else:

            self.grid = [
                list(row) for row in DEFAULT_MAP
            ]

            self.key_pos = (2, 2)
            self.vault_pos = (10, 2)
            self.artifact_pos = (11, 2)
            self.exit_pos = (13, 9)

            self.thief_start = (1, 1)
            self.guard_start = (13, 1)

        self.cols = len(self.grid[0])
        self.rows = len(self.grid)

    def in_bounds(self, pos):

        x, y = pos

        return (
            0 <= x < self.cols
            and 0 <= y < self.rows
        )

    def tile_at(self, pos):

        x, y = pos

        if not self.in_bounds(pos):
            return "W"

        return self.grid[y][x]

    def is_walkable(self, pos, vault_unlocked=False):

        if not self.in_bounds(pos):
            return False

        tile = self.tile_at(pos)

        if tile == "W":
            return False

        if tile == "D" and not vault_unlocked:
            return False

        return True

    def neighbors(self, pos, vault_unlocked=False):

        x, y = pos

        possible_moves = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        for next_pos in possible_moves:

            if self.is_walkable(
                next_pos,
                vault_unlocked
            ):

                yield next_pos

from config import MAX_ROUNDS, PURPLE, CYAN

from game.board import Board
from game.player import Player
from algorithms.bfs import bfs


class GameState:

    def __init__(self, mode="2p"):

        self.board = Board(use_generated=True, seed=None)

        self.thief = Player(
            "THIEF",
            self.board.thief_start,
            PURPLE
        )

        self.guard = Player(
            "GUARD",
            self.board.guard_start,
            CYAN
        )

        self.mode = mode

        self.turn = "thief"
        self.round = 1

        self.has_key = False
        self.vault_unlocked = False
        self.has_artifact = False

        self.game_over = False
        self.result = None

        self.log = [
            "Mission started. Thief moves first."
        ]

        # MEDIUM AI SETTINGS
        self.ai_vision_range = 4

        self.last_known_position = None
        self.search_turns_remaining = 0

        self.ai_patrol_index = 0

        self.patrol_points = [
            self.board.key_pos,
            self.board.vault_pos,
            self.board.artifact_pos,
            self.board.exit_pos
        ]

        self.ai_move_count = 0

    # --------------------------------
    # GAME MESSAGES
    # --------------------------------

    def say(self, message):

        self.log.append(message)
        self.log = self.log[-6:]

    # --------------------------------
    # FINISH GAME
    # --------------------------------

    def finish(self, winner, reason):

        self.game_over = True

        self.result = {
            "winner": winner,
            "reason": reason,
            "rounds": self.round,
            "artifact": self.has_artifact,
            "key": self.has_key
        }

    # --------------------------------
    # THIEF OBJECTIVES
    # --------------------------------

    def resolve_thief_tile(self):

        if (
            self.thief.position == self.board.key_pos
            and not self.has_key
        ):

            self.has_key = True
            self.say("Thief collected the vault key.")

        if (
            self.thief.position == self.board.vault_pos
            and self.has_key
            and not self.vault_unlocked
        ):

            self.vault_unlocked = True
            self.say("Vault unlocked.")

        if (
            self.thief.position == self.board.artifact_pos
            and self.vault_unlocked
            and not self.has_artifact
        ):

            self.has_artifact = True
            self.say("Artifact secured! Reach the exit.")

        if (
            self.thief.position == self.board.exit_pos
            and self.has_artifact
        ):

            self.finish(
                "THIEF",
                "The thief escaped with the artifact."
            )

    # --------------------------------
    # CAPTURE CHECK
    # --------------------------------

    def check_capture(self):

        if self.thief.position == self.guard.position:

            self.finish(
                "GUARD",
                "The guard captured the thief."
            )

    # --------------------------------
    # PLAYER MOVEMENT
    # --------------------------------

    def move(self, player_name, dx, dy):

        if self.game_over:
            return

        if player_name != self.turn:
            return

        if player_name == "thief":
            player = self.thief

        elif player_name == "guard":
            player = self.guard

        else:
            return

        target = (
            player.position[0] + dx,
            player.position[1] + dy
        )

        if (
            player_name == "thief"
            and target == self.board.vault_pos
            and self.has_key
        ):

            self.vault_unlocked = True
            self.say("Vault unlocked with the key.")

        if not self.board.is_walkable(
            target,
            self.vault_unlocked
        ):

            self.say("Blocked: wall or locked vault door.")
            return

        player.move_to(target)

        if player_name == "thief":

            self.resolve_thief_tile()

        self.check_capture()

        if self.game_over:
            return

        if player_name == "thief":

            self.turn = "guard"

            if self.mode == "ai":

                self.ai_guard_move()

        else:

            self.turn = "thief"
            self.round += 1

            if self.round > MAX_ROUNDS:

                self.finish(
                    "GUARD",
                    "The thief ran out of time."
                )

            else:

                self.say(
                    f"Round {self.round}: thief's turn."
                )

    # --------------------------------
    # AI: LINE OF SIGHT
    # --------------------------------

    def has_line_of_sight(self, start, end):

        x1, y1 = start
        x2, y2 = end

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        error = dx - dy

        x, y = x1, y1

        while (x, y) != (x2, y2):

            e2 = 2 * error

            if e2 > -dy:
                error -= dy
                x += sx

            if e2 < dx:
                error += dx
                y += sy

            current = (x, y)

            # The thief's tile itself is visible.
            if current == end:
                return True

            # Walls and locked doors block vision.
            tile = self.board.tile_at(current)

            if tile == "W":
                return False

            if tile == "D" and not self.vault_unlocked:
                return False

        return True

    # --------------------------------
    # AI: DETECT THIEF
    # --------------------------------

    def can_detect_thief(self):

        gx, gy = self.guard.position
        tx, ty = self.thief.position

        distance = abs(gx - tx) + abs(gy - ty)

        if distance > self.ai_vision_range:
            return False

        return self.has_line_of_sight(
            self.guard.position,
            self.thief.position
        )

    # --------------------------------
    # AI: CHOOSE NEXT STEP USING BFS
    # --------------------------------

    def get_next_step(self, target):

        path = bfs(
            self.board,
            self.guard.position,
            target,
            self.vault_unlocked
        )

        if path and len(path) > 1:
            return path[1]

        return None

    # --------------------------------
    # AI: MOVE TOWARDS TARGET
    # --------------------------------

    def move_guard_towards(self, target):

        next_step = self.get_next_step(target)

        if next_step is None:
            return False

        self.guard.move_to(next_step)

        self.check_capture()

        return True

    # --------------------------------
    # AI: PATROL MUSEUM
    # --------------------------------

    def patrol_museum(self):

        # Visit key, vault, artifact and exit areas.
        attempts = 0

        while attempts < len(self.patrol_points):

            target = self.patrol_points[
                self.ai_patrol_index
            ]

            if self.guard.position == target:

                self.ai_patrol_index = (
                    self.ai_patrol_index + 1
                ) % len(self.patrol_points)

                target = self.patrol_points[
                    self.ai_patrol_index
                ]

            if self.move_guard_towards(target):
                self.say("AI guard is patrolling the museum.")
                return

            self.ai_patrol_index = (
                self.ai_patrol_index + 1
            ) % len(self.patrol_points)

            attempts += 1

        self.say("AI guard is searching the museum.")

    # --------------------------------
    # AI: MEDIUM DIFFICULTY
    # --------------------------------

    def ai_guard_move(self):

        if self.game_over:
            return

        self.ai_move_count += 1

        # CASE 1: Thief is visible.
        if self.can_detect_thief():

            self.last_known_position = self.thief.position

            self.search_turns_remaining = 2

            self.say("AI guard spotted the thief!")

            self.move_guard_towards(
                self.last_known_position
            )

        # CASE 2: Thief is no longer visible.
        elif self.search_turns_remaining > 0:

            self.say(
                "AI guard is investigating the last known position."
            )

            target = self.last_known_position

            self.move_guard_towards(target)

            self.search_turns_remaining -= 1

        # CASE 3: No detection. Patrol the museum.
        else:

            self.patrol_museum()

        # Check capture after AI movement.
        self.check_capture()

        # Return control to thief.
        if not self.game_over:

            self.turn = "thief"
            self.round += 1

            if self.round > MAX_ROUNDS:

                self.finish(
                    "GUARD",
                    "The thief ran out of time."
                )

            else:

                self.say(
                    f"Round {self.round}: thief's turn."
                )

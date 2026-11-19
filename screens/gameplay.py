
import pygame

from config import *

from game.game_state import GameState
from game.renderer import BoardRenderer
from game.audio_manager import AudioManager


class GameplayScreen:

    def __init__(self, mode="2p"):

        self.state = GameState(mode)

        self.renderer = BoardRenderer()

        # Audio setup
        self.audio = AudioManager()

        self.audio.play_music("bgm_gameplay.wav")

        self.result_sound_played = False

        # Fonts
        self.title_font = pygame.font.SysFont(
            "consolas", 30, bold=True
        )

        self.heading_font = pygame.font.SysFont(
            "consolas", 21, bold=True
        )

        self.font = pygame.font.SysFont(
            "consolas", 17
        )

        self.small_font = pygame.font.SysFont(
            "consolas", 14
        )

    # -----------------------------------------
    # TEXT HELPER
    # -----------------------------------------

    def draw_text(
        self,
        surface,
        message,
        x,
        y,
        font=None,
        color=WHITE
    ):

        if font is None:
            font = self.font

        rendered = font.render(
            str(message),
            True,
            color
        )

        surface.blit(rendered, (x, y))

    # -----------------------------------------
    # PLAYER MOVEMENT WITH SOUND
    # -----------------------------------------

    def perform_move(self, player, dx, dy):

        if self.state.game_over:
            return

        if player == "thief":

            old_position = self.state.thief.position

        else:

            old_position = self.state.guard.position

        old_key = self.state.has_key
        old_vault = self.state.vault_unlocked
        old_artifact = self.state.has_artifact

        # Perform actual game movement
        self.state.move(player, dx, dy)

        if player == "thief":

            new_position = self.state.thief.position

        else:

            new_position = self.state.guard.position

        # Movement sound
        if old_position != new_position:

            self.audio.play("move")

        # Collection sound
        if (
            old_key != self.state.has_key
            or old_artifact != self.state.has_artifact
        ):

            self.audio.play("collect")

        # Vault opening sound
        if old_vault != self.state.vault_unlocked:

            self.audio.play("door_open")

    # -----------------------------------------
    # INPUT HANDLING
    # -----------------------------------------

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.audio.stop_music()
                return "menu"

            if self.state.game_over:
                return None

            # THIEF CONTROLS
            if self.state.turn == "thief":

                moves = {

                    pygame.K_w: (0, -1),
                    pygame.K_s: (0, 1),
                    pygame.K_a: (-1, 0),
                    pygame.K_d: (1, 0)

                }

                if event.key in moves:

                    dx, dy = moves[event.key]

                    self.perform_move(
                        "thief",
                        dx,
                        dy
                    )

            # HUMAN GUARD CONTROLS
            elif self.state.mode == "2p":

                moves = {

                    pygame.K_UP: (0, -1),
                    pygame.K_DOWN: (0, 1),
                    pygame.K_LEFT: (-1, 0),
                    pygame.K_RIGHT: (1, 0)

                }

                if event.key in moves:

                    dx, dy = moves[event.key]

                    self.perform_move(
                        "guard",
                        dx,
                        dy
                    )

        return None

    # -----------------------------------------
    # UPDATE GAME
    # -----------------------------------------

    def update(self, dt):

        if self.state.game_over:

            if not self.result_sound_played:

                if self.state.result["winner"] == "THIEF":

                    self.audio.play("victory")

                else:

                    self.audio.play("defeat")

                self.result_sound_played = True

                self.audio.stop_music()

            return (
                "result",
                self.state.result
            )

        return None

    # -----------------------------------------
    # HEADER
    # -----------------------------------------

    def draw_header(self, surface):

        self.draw_text(
            surface,
            "THE GREAT HEIST",
            45,
            22,
            self.title_font,
            PURPLE
        )

        self.draw_text(
            surface,
            "MUSEUM SECURITY SYSTEM",
            50,
            62,
            self.small_font,
            MUTED
        )

        pygame.draw.line(
            surface,
            GRID,
            (45, 82),
            (1235, 82),
            2
        )

        mode_label = (
            "2 PLAYER MODE"
            if self.state.mode == "2p"
            else "AI GUARD MODE"
        )

        self.draw_text(
            surface,
            mode_label,
            1050,
            35,
            self.font,
            CYAN
        )

    # -----------------------------------------
    # INFORMATION PANEL
    # -----------------------------------------

    def draw_panel(self, surface):

        panel_rect = pygame.Rect(
            790,
            95,
            445,
            575
        )

        pygame.draw.rect(
            surface,
            PANEL,
            panel_rect,
            border_radius=12
        )

        pygame.draw.rect(
            surface,
            GRID,
            panel_rect,
            2,
            border_radius=12
        )

        self.draw_text(
            surface,
            "MISSION STATUS",
            815,
            115,
            self.heading_font,
            WHITE
        )

        self.draw_text(
            surface,
            f"ROUND {self.state.round} / {MAX_ROUNDS}",
            815,
            155,
            self.font,
            YELLOW
        )

        # Current turn
        if self.state.turn == "thief":

            turn_label = "THIEF'S TURN"
            turn_color = PURPLE

        else:

            turn_label = "GUARD'S TURN"
            turn_color = CYAN

        turn_rect = pygame.Rect(
            815,
            190,
            395,
            38
        )

        pygame.draw.rect(
            surface,
            PANEL_LIGHT,
            turn_rect,
            border_radius=6
        )

        self.draw_text(
            surface,
            turn_label,
            830,
            199,
            self.font,
            turn_color
        )

        # Inventory
        self.draw_text(
            surface,
            "INVENTORY",
            815,
            250,
            self.heading_font,
            WHITE
        )

        inventory_items = [

            ("KEY", self.state.has_key, YELLOW),

            ("VAULT", self.state.vault_unlocked, ORANGE),

            ("ARTIFACT", self.state.has_artifact, GREEN)

        ]

        for index, (name, collected, color) in enumerate(
            inventory_items
        ):

            y = 290 + index * 38

            status = (
                "COLLECTED"
                if collected
                else "PENDING"
            )

            status_color = (
                GREEN
                if collected
                else MUTED
            )

            pygame.draw.circle(
                surface,
                color,
                (825, y + 9),
                6
            )

            self.draw_text(
                surface,
                name,
                845,
                y,
                self.font,
                WHITE
            )

            self.draw_text(
                surface,
                status,
                1060,
                y,
                self.small_font,
                status_color
            )

        # Mission objectives
        self.draw_text(
            surface,
            "MISSION OBJECTIVES",
            815,
            415,
            self.heading_font,
            WHITE
        )

        objectives = [

            ("Collect the key", self.state.has_key),

            ("Unlock the vault", self.state.vault_unlocked),

            ("Collect the artifact", self.state.has_artifact),

            (
                "Escape the museum",
                self.state.game_over
                and self.state.result["winner"] == "THIEF"
            )

        ]

        for index, (objective, completed) in enumerate(
            objectives
        ):

            y = 453 + index * 28

            marker = "✓" if completed else "○"

            color = GREEN if completed else MUTED

            self.draw_text(
                surface,
                f"{marker}  {objective}",
                820,
                y,
                self.small_font,
                color
            )



    # -----------------------------------------
    # CONTROLS
    # -----------------------------------------

    def draw_controls(self, surface):

        y = 645

        self.draw_text(
            surface,
            "THIEF: W A S D",
            45,
            y,
            self.small_font,
            PURPLE
        )

        if self.state.mode == "2p":

            self.draw_text(
                surface,
                "GUARD: ARROW KEYS",
                260,
                y,
                self.small_font,
                CYAN
            )

        else:

            self.draw_text(
                surface,
                "GUARD: AI CONTROLLED",
                260,
                y,
                self.small_font,
                CYAN
            )

        self.draw_text(
            surface,
            "ESC: MAIN MENU",
            540,
            y,
            self.small_font,
            MUTED
        )

    # -----------------------------------------
    # MAIN DRAW FUNCTION
    # -----------------------------------------

    def draw(self, surface):

        surface.fill(BACKGROUND)

        self.draw_header(surface)

        self.renderer.draw(
            surface,
            self.state
        )

        self.draw_panel(surface)

        self.draw_controls(surface)

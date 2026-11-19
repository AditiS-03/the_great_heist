
import pygame
from pathlib import Path

from config import *
from screens.common import text, button


class ResultsScreen:

    def __init__(self, result):

        self.result = result or {
            "winner": "—",
            "reason": "Game ended."
        }

        project_root = Path(__file__).resolve().parent.parent

        background_path = (
            project_root
            / "assets"
            / "images"
            / "menu_background.png"
        )

        self.background = None

        if background_path.exists():
            try:
                self.background = pygame.image.load(
                    str(background_path)
                ).convert()

                self.background = pygame.transform.scale(
                    self.background,
                    (SCREEN_WIDTH, SCREEN_HEIGHT)
                )

            except pygame.error as error:
                print("Results background error:", error)

        self.replay = pygame.Rect(
            350, 500, 250, 60
        )

        self.menu = pygame.Rect(
            680, 500, 250, 60
        )

    # --------------------------------
    # EVENT HANDLING
    # --------------------------------

    def handle_event(self, event):

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            if self.replay.collidepoint(event.pos):
                return "replay"

            if self.menu.collidepoint(event.pos):
                return "menu"

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                return "replay"

            if event.key == pygame.K_ESCAPE:
                return "menu"

        return None

    # --------------------------------
    # BACKGROUND
    # --------------------------------

    def draw_background(self, surface):

        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill(BACKGROUND)

        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((10, 15, 30, 175))
        surface.blit(overlay, (0, 0))

    # --------------------------------
    # RESULTS PAGE
    # --------------------------------

    def draw(self, surface):

        self.draw_background(surface)

        winner = self.result.get(
            "winner",
            "—"
        )

        color = (
            PURPLE
            if winner == "THIEF"
            else CYAN
        )

        text(
            surface,
            "MISSION COMPLETE",
            420, 170, 38, WHITE, True
        )

        text(
            surface,
            f"{winner} WINS",
            500, 255, 42, color, True
        )

        text(
            surface,
            self.result.get("reason", ""),
            380, 340, 20, MUTED
        )

        text(
            surface,
            f"Rounds played: {self.result.get('rounds', '—')}",
            480, 390, 20, WHITE
        )

        button(
            surface,
            self.replay,
            "PLAY AGAIN"
        )

        button(
            surface,
            self.menu,
            "MAIN MENU"
        )


import pygame
from pathlib import Path

from config import *
from screens.common import text, button


class BriefingScreen:

    def __init__(self):

        project_root = Path(__file__).resolve().parent.parent

        background_path = (
            project_root
            / "assets"
            / "images"
            / "briefing.png"
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
                print("Briefing background error:", error)

        self.start_rect = pygame.Rect(
            470, 555, 340, 60
        )

        self.rules_rect = pygame.Rect(
            1040, 35, 180, 48
        )

        self.back_rect = pygame.Rect(
            45, 35, 160, 48
        )

        self.show_rules = False

    # --------------------------------
    # EVENT HANDLING
    # --------------------------------

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if self.show_rules:
                    self.show_rules = False
                    return None

                return "menu"

            if self.show_rules:
                return None

            if event.key in (
                pygame.K_RETURN,
                pygame.K_SPACE
            ):
                return "start"

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            if self.show_rules:

                if self.back_rect.collidepoint(event.pos):
                    self.show_rules = False

                return None

            if self.rules_rect.collidepoint(event.pos):
                self.show_rules = True
                return None

            if self.start_rect.collidepoint(event.pos):
                return "start"

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
    # BRIEFING PAGE
    # --------------------------------

    def draw_briefing(self, surface):

        text(
            surface,
            "MISSION BRIEFING",
            430, 90, 38, PURPLE, True
        )

        # Thief objectives
        text(
            surface,
            "THIEF OBJECTIVE",
            160, 190, 24, PURPLE, True
        )

        text(surface, "1. Collect the yellow key.", 160, 240, 21)
        text(surface, "2. Reach the orange vault.", 160, 280, 21)
        text(surface, "3. Collect the artifact.", 160, 320, 21)
        text(surface, "4. Escape through the green exit.", 160, 360, 21)

        # Guard objectives
        text(
            surface,
            "GUARD OBJECTIVE",
            690, 190, 24, CYAN, True
        )

        text(
            surface,
            "Capture the thief by entering",
            690, 240, 21
        )

        text(
            surface,
            "the same grid position.",
            690, 280, 21
        )

        text(
            surface,
            "The thief has 30 rounds.",
            690, 320, 21
        )

        text(
            surface,
            "Each turn allows one tile of movement.",
            320, 450, 21, MUTED
        )

        button(
            surface,
            self.rules_rect,
            "RULES"
        )

        button(
            surface,
            self.start_rect,
            "START MISSION"
        )

    # --------------------------------
    # RULES PAGE
    # --------------------------------

    def draw_rules(self, surface):

        button(
            surface,
            self.back_rect,
            "BACK"
        )

        text(
            surface,
            "GAME RULES",
            475, 65, 38, PURPLE, True
        )

        text(
            surface,
            "OBJECTIVE",
            130, 145, 23, YELLOW, True
        )

        text(
            surface,
            "The thief must collect the key, unlock the vault,",
            130, 185, 19, WHITE
        )

        text(
            surface,
            "steal the artifact and escape through the exit.",
            130, 220, 19, WHITE
        )

        text(
            surface,
            "MOVEMENT AND TURNS",
            130, 280, 23, CYAN, True
        )

        text(
            surface,
            "1. The thief gets the first turn.",
            130, 320, 19, WHITE
        )

        text(
            surface,
            "2. Each player can move one tile per turn.",
            130, 355, 19, WHITE
        )

        text(
            surface,
            "3. Walls block movement.",
            130, 390, 19, WHITE
        )

        text(
            surface,
            "4. The guard cannot cross a locked vault door.",
            130, 425, 19, WHITE
        )

        text(
            surface,
            "WINNING AND LOSING",
            130, 485, 23, PURPLE, True
        )

        text(
            surface,
            "• Thief wins by escaping with the artifact.",
            130, 525, 19, WHITE
        )

        text(
            surface,
            "• Guard wins by capturing the thief.",
            130, 560, 19, WHITE
        )

        text(
            surface,
            "• The guard also wins if the 30-round limit expires.",
            130, 595, 19, WHITE
        )

        text(
            surface,
            "CONTROLS: Thief - W A S D | Guard - Arrow Keys",
            260, 655, 18, YELLOW, True
        )

    # --------------------------------
    # MAIN DRAW
    # --------------------------------

    def draw(self, surface):

        self.draw_background(surface)

        if self.show_rules:
            self.draw_rules(surface)
        else:
            self.draw_briefing(surface)

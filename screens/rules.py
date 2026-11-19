
import pygame

from config import *


class RulesScreen:

    def __init__(self):

        self.title_font = pygame.font.SysFont(
            "consolas", 34, bold=True
        )

        self.heading_font = pygame.font.SysFont(
            "consolas", 21, bold=True
        )

        self.font = pygame.font.SysFont(
            "consolas", 16
        )

        self.small_font = pygame.font.SysFont(
            "consolas", 14
        )

        self.back_button = pygame.Rect(
            45, 640, 180, 45
        )

    def draw_text(
        self, surface, message, x, y,
        font=None, color=WHITE
    ):

        if font is None:
            font = self.font

        rendered = font.render(
            message, True, color
        )

        surface.blit(rendered, (x, y))

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                return "menu"

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            if self.back_button.collidepoint(event.pos):
                return "menu"

        return None

    def draw_section(
        self, surface, heading, lines,
        x, y, color=PURPLE
    ):

        self.draw_text(
            surface,
            heading,
            x,
            y,
            self.heading_font,
            color
        )

        y += 34

        for line in lines:

            self.draw_text(
                surface,
                line,
                x + 5,
                y,
                self.font,
                WHITE
            )

            y += 25

        return y

    def draw(self, surface):

        surface.fill(BACKGROUND)

        # Header
        self.draw_text(
            surface,
            "HOW TO PLAY",
            45, 25,
            self.title_font,
            PURPLE
        )

        self.draw_text(
            surface,
            "THE GREAT HEIST - MISSION RULEBOOK",
            50, 72,
            self.small_font,
            MUTED
        )

        pygame.draw.line(
            surface,
            GRID,
            (45, 105),
            (1235, 105),
            2
        )

        # LEFT COLUMN
        self.draw_section(
            surface,
            "1. GAME OBJECTIVE",
            [
                "Play as a thief trying to steal a museum artifact.",
                "The security guard must stop the thief.",
                "The thief must collect the artifact and escape.",
                "The guard wins by capturing the thief."
            ],
            55, 130,
            PURPLE
        )

        self.draw_section(
            surface,
            "2. THIEF CONTROLS",
            [
                "W - Move up",
                "S - Move down",
                "A - Move left",
                "D - Move right",
                "Move one tile per turn."
            ],
            55, 280,
            PURPLE
        )

        self.draw_section(
            surface,
            "3. GUARD CONTROLS",
            [
                "UP ARROW - Move up",
                "DOWN ARROW - Move down",
                "LEFT ARROW - Move left",
                "RIGHT ARROW - Move right",
                "The guard tries to capture the thief."
            ],
            55, 460,
            CYAN
        )

        # RIGHT COLUMN
        self.draw_section(
            surface,
            "4. THIEF MISSION SEQUENCE",
            [
                "1. Find and collect the golden key.",
                "2. Reach the locked museum vault.",
                "3. Unlock the vault using the key.",
                "4. Collect the valuable artifact.",
                "5. Reach the green exit to escape."
            ],
            660, 130,
            YELLOW
        )

        self.draw_section(
            surface,
            "5. TURN SYSTEM",
            [
                "1. The thief takes the first turn.",
                "2. The guard takes the next turn.",
                "3. Players move one tile per turn.",
                "4. A round completes after both turns.",
                "5. The mission has a limited number of rounds."
            ],
            660, 305,
            CYAN
        )

        self.draw_section(
            surface,
            "6. IMPORTANT RULES",
            [
                "Walls cannot be crossed.",
                "Locked vault doors block movement.",
                "The key is needed to unlock the vault.",
                "The artifact must be collected before escape.",
                "Touching the guard results in capture.",
                "The thief must escape before the round limit."
            ],
            660, 490,
            ORANGE
        )

        # Back button
        pygame.draw.rect(
            surface,
            PANEL,
            self.back_button,
            border_radius=8
        )

        pygame.draw.rect(
            surface,
            PURPLE,
            self.back_button,
            2,
            border_radius=8
        )

        self.draw_text(
            surface,
            "BACK TO MENU",
            self.back_button.x + 17,
            self.back_button.y + 12,
            self.font,
            WHITE
        )

        self.draw_text(
            surface,
            "Press ESC to return",
            260, 653,
            self.small_font,
            MUTED
        )

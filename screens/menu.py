
import pygame
from pathlib import Path

from config import *

from screens.common import text, button

from game.audio_manager import AudioManager


class MenuScreen:

    def __init__(self):

        self.audio = AudioManager()

        # Play menu background music
        self.audio.play_music("bgm_menu.wav")

        # Load menu background
        project_root = (
            Path(__file__).resolve().parent.parent
        )

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

                print("Could not load menu background:", error)

        else:

            print("menu_background.png was not found.")

        # Menu buttons
        self.buttons = [

            (
                pygame.Rect(470, 330, 340, 60),
                "2p"
            ),

            (
                pygame.Rect(470, 420, 340, 60),
                "ai"
            )

        ]

    # -----------------------------------------
    # INPUT
    # -----------------------------------------

    def handle_event(self, event):

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            for rect, action in self.buttons:

                if rect.collidepoint(event.pos):

                    self.audio.play("button_click")

                    return action

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:

                self.audio.play("button_click")
                return "2p"

            if event.key == pygame.K_2:

                self.audio.play("button_click")
                return "ai"

        return None

    # -----------------------------------------
    # DRAW
    # -----------------------------------------

    def draw(self, surface):

        # Draw background image
        if self.background:

            surface.blit(
                self.background,
                (0, 0)
            )

        else:

            surface.fill(BACKGROUND)

        # Add dark transparent overlay
        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((5, 10, 25, 125))

        surface.blit(
            overlay,
            (0, 0)
        )

        # Game title
        text(
            surface,
            "THE GREAT HEIST",
            460,
            150,
            48,
            PURPLE,
            True
        )

        text(
            surface,
            "A TURN-BASED MUSEUM STEALTH STRATEGY GAME",
            410,
            225,
            20,
            WHITE
        )

        # Menu buttons
        for rect, action in self.buttons:

            labels = {

                "2p": "PLAY 2 PLAYERS",

                "ai": "PLAY VS AI GUARD"

            }

            button(
                surface,
                rect,
                labels[action]
            )

        text(
            surface,
            "1: TWO PLAYERS     2: PLAY AGAINST AI",
            460,
            540,
            18,
            WHITE
        )

        text(
            surface,
            "THIEF: W A S D",
            490,
            590,
            18,
            PURPLE
        )

        text(
            surface,
            "GUARD: ARROW KEYS",
            490,
            620,
            18,
            CYAN
        )

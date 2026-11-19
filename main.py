
import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    GAME_TITLE,
    BACKGROUND
)

from screens.menu import MenuScreen
from screens.rules import RulesScreen
from screens.briefing import BriefingScreen
from screens.gameplay import GameplayScreen
from screens.results import ResultsScreen


def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    pygame.display.set_caption(GAME_TITLE)

    clock = pygame.time.Clock()

    # Initial screen
    current_screen = MenuScreen()

    rules_screen = RulesScreen()

    game_mode = "2p"

    running = True

    while running:

        dt = clock.tick(FPS) / 1000

        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:

                running = False
                break

            action = current_screen.handle_event(event)

            if action is None:
                continue

            # Open two-player or AI mode briefing
            if action in ("2p", "ai"):

                game_mode = action

                current_screen = BriefingScreen()

            # Open rules screen
            elif action == "rules":

                current_screen = rules_screen

            # Return to menu
            elif action == "menu":

                current_screen = MenuScreen()

            # Start mission
            elif action == "start":

                current_screen = GameplayScreen(
                    mode=game_mode
                )

            # Replay mission
            elif action == "replay":

                current_screen = GameplayScreen(
                    mode=game_mode
                )

            # Handle results
            elif isinstance(action, tuple):

                if action[0] == "result":

                    current_screen = ResultsScreen(
                        action[1]
                    )

        if not running:
            break

        # Update current screen
        if hasattr(current_screen, "update"):

            action = current_screen.update(dt)

            if action and isinstance(action, tuple):

                if action[0] == "result":

                    current_screen = ResultsScreen(
                        action[1]
                    )

        # Render screen
        screen.fill(BACKGROUND)

        current_screen.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":

    main()

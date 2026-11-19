
import pygame
from pathlib import Path

from config import *


class BoardRenderer:

    def __init__(self):
        project_root = Path(__file__).resolve().parent.parent
        self.assets_dir = project_root / "assets" / "images"

        self.sprites = {}
        self.load_sprites()

    def load_image(self, filename, size, crop_transparent=False):

        path = self.assets_dir / filename

        if not path.exists():
            print(f"Asset not found: {path}")
            return None

        try:
            image = pygame.image.load(str(path)).convert_alpha()

            # Remove unnecessary transparent padding
            if crop_transparent:
                bounding_rect = image.get_bounding_rect(min_alpha=10)

                if bounding_rect.width > 0 and bounding_rect.height > 0:
                    image = image.subsurface(bounding_rect).copy()

            # Scale while preserving crisp pixel edges
            image = pygame.transform.scale(image, size)

            return image

        except pygame.error as error:
            print(f"Could not load {filename}: {error}")
            return None

    def load_sprites(self):

        # Character sprites
        self.sprites["thief"] = self.load_image(
            "thief.png", (44, 44), True
        )

        self.sprites["guard"] = self.load_image(
            "guard.png", (44, 44), True
        )

        # Museum tiles
        self.sprites["floor"] = self.load_image(
            "floor.png", (48, 48)
        )

        self.sprites["wall"] = self.load_image(
            "wall.png", (48, 48)
        )

        # Mission objects
        self.sprites["key"] = self.load_image(
            "key.png", (34, 34), True
        )

        self.sprites["artifact"] = self.load_image(
            "artifact.png", (40, 40), True
        )

        # Vault and exit
        self.sprites["vault"] = self.load_image(
            "vault.png", (48, 48)
        )

        self.sprites["exit"] = self.load_image(
            "exit.png", (48, 48)
        )

        self.sprites["vault_open"] = self.load_image(
            "vault_open.png", (48, 48)
        )

    def draw_tile(self, surface, x, y, tile):

        rect = pygame.Rect(
            BOARD_X + x * TILE_SIZE,
            BOARD_Y + y * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

        if tile == "W":
            image = self.sprites["wall"]
            fallback_color = WALL
        else:
            image = self.sprites["floor"]
            fallback_color = FLOOR

        if image:
            surface.blit(image, rect.topleft)
        else:
            pygame.draw.rect(surface, fallback_color, rect)

        pygame.draw.rect(surface, GRID, rect, 1)

    def draw_object(self, surface, pos, image_name, fallback_color):

        x, y = pos

        center_x = BOARD_X + x * TILE_SIZE + TILE_SIZE // 2
        center_y = BOARD_Y + y * TILE_SIZE + TILE_SIZE // 2

        image = self.sprites.get(image_name)

        if image:
            rect = image.get_rect(center=(center_x, center_y))
            surface.blit(image, rect)
        else:
            pygame.draw.circle(
                surface,
                fallback_color,
                (center_x, center_y),
                13
            )

    def draw_player(self, surface, player, sprite_name, active):

        x, y = player.position

        tile_x = BOARD_X + x * TILE_SIZE
        tile_y = BOARD_Y + y * TILE_SIZE

        # Highlight active player's tile
        if active:
            highlight = pygame.Rect(
                tile_x + 2,
                tile_y + 2,
                TILE_SIZE - 4,
                TILE_SIZE - 4
            )

            pygame.draw.rect(
                surface,
                YELLOW,
                highlight,
                2
            )

        image = self.sprites.get(sprite_name)

        if image:
            # Center sprite inside its tile
            rect = image.get_rect(
                center=(
                    tile_x + TILE_SIZE // 2,
                    tile_y + TILE_SIZE // 2
                )
            )

            surface.blit(image, rect)

        else:
            pygame.draw.circle(
                surface,
                player.color,
                (
                    tile_x + TILE_SIZE // 2,
                    tile_y + TILE_SIZE // 2
                ),
                17
            )

    def draw(self, surface, state):

        board = state.board

        # Draw floor and walls
        for y, row in enumerate(board.grid):
            for x, tile in enumerate(row):
                self.draw_tile(surface, x, y, tile)

        # Draw vault
        vault_image_name = (
            "vault_open"
            if state.vault_unlocked
            and self.sprites.get("vault_open")
            else "vault"
        )

        self.draw_object(
            surface,
            board.vault_pos,
            vault_image_name,
            ORANGE
        )

        # Draw key
        if not state.has_key:
            self.draw_object(
                surface,
                board.key_pos,
                "key",
                YELLOW
            )

        # Draw artifact
        if not state.has_artifact:
            self.draw_object(
                surface,
                board.artifact_pos,
                "artifact",
                ORANGE
            )

        # Draw exit
        self.draw_object(
            surface,
            board.exit_pos,
            "exit",
            GREEN
        )

        # Draw players last
        self.draw_player(
            surface,
            state.thief,
            "thief",
            state.turn == "thief"
        )

        self.draw_player(
            surface,
            state.guard,
            "guard",
            state.turn == "guard"
        )

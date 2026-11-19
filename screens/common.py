import pygame

from config import *


def text(
    surface,
    value,
    x,
    y,
    size=22,
    color=WHITE,
    bold=False
):

    font = pygame.font.SysFont(
        "consolas",
        size,
        bold=bold
    )

    rendered = font.render(
        str(value),
        True,
        color
    )

    surface.blit(rendered, (x, y))


def button(
    surface,
    rect,
    label,
    active=False
):

    color = (
        (54, 75, 105)
        if active
        else PANEL_LIGHT
    )

    pygame.draw.rect(
        surface,
        color,
        rect,
        border_radius=8
    )

    pygame.draw.rect(
        surface,
        CYAN if active else GRID,
        rect,
        2,
        border_radius=8
    )

    font = pygame.font.SysFont(
        "consolas",
        20,
        bold=True
    )

    rendered = font.render(
        label,
        True,
        WHITE
    )

    surface.blit(
        rendered,
        rendered.get_rect(center=rect.center)
    )
import numpy as np
import pygame

from .display_type import ColorMode
from .game_mode import GameMode

LIFE_THRESHOLD = 0.5
COLOR_ALPHA = 1.0


def color_entangled(cell):
    # TODO: Write function for calculating color in entangled mode
    color = pygame.Color(0, 0, 0)
    # print(angle*180/np.pi, 0, int(mag * 100), COLOR_ALPHA)
    # print((cell["angle"], 0, int(cell["mag"] * 100), COLOR_ALPHA))
    color.hsva = (cell["angle"], cell["sat"], int(cell["mag"] * 100), COLOR_ALPHA)
    return color


def color_hamiltonian(cell):
    color_h = int(np.angle(cell["alive"], deg=True) % 360)
    color_s = int(100 * np.abs(cell["alive"]))
    if np.abs(cell["alive"]) ** 2 > LIFE_THRESHOLD:
        color_v = 100
    else:
        color_v = 0
    color = pygame.Color(0, 0, 0)
    color.hsva = (color_h, color_s, color_v, COLOR_ALPHA)
    return color


def color_functional(cell, color_mode_h, color_mode_s, color_mode_v):
    color = pygame.Color(0, 0, 0)
    # Set defaults for if no mode is selected
    if color_mode_h == None:
        color_mode_h = ColorMode.DELTA_PHASE_BA
    if color_mode_s == None:
        color_mode_s = ColorMode.CONST
    if color_mode_v == None:
        color_mode_v = ColorMode.B_ABS
    color_h = 0
    color_s = 0
    color_v = 0
    match color_mode_h:
        case ColorMode.A_MOD:
            color_h = int(360 * np.abs(cell["dead"]))
        case ColorMode.B_ABS:
            color_h = int(360 * np.abs(cell["alive"]))
        case ColorMode.A_PHASE:
            color_h = int(np.angle(cell["dead"], deg=True) % 360)
        case ColorMode.B_PHASE:
            color_h = int(np.angle(cell["alive"], deg=True) % 360)
        case ColorMode.DELTA_PHASE_BA:
            color_h = int(
                (np.angle(cell["alive"], deg=True) - np.angle(cell["dead"], deg=True))
                % 360
            )
        case ColorMode.DELTA_PHASE_AB:
            color_h = int(
                (np.angle(cell["dead"], deg=True) - np.angle(cell["alive"], deg=True))
                % 360
            )
        case ColorMode.CONST:
            color_h = 0
        case _:
            print("not allowed")
    match color_mode_s:
        case ColorMode.A_MOD:
            color_s = int(100 * np.abs(cell["dead"]))
        case ColorMode.B_ABS:
            color_s = int(100 * np.abs(cell["alive"]))
        case ColorMode.A_PHASE:
            color_s = int((100.0 / 360.0) * (np.angle(cell["dead"], deg=True) % 360))
        case ColorMode.B_PHASE:
            color_s = int((100.0 / 360.0) * (np.angle(cell["alive"], deg=True) % 360))
        case ColorMode.DELTA_PHASE_BA:
            color_s = int(
                (100.0 / 360.0)
                * (
                    (
                        np.angle(cell["alive"], deg=True)
                        - np.angle(cell["dead"], deg=True)
                    )
                    % 360
                )
            )
        case ColorMode.DELTA_PHASE_AB:
            color_s = int(
                (100.0 / 360.0)
                * (
                    (
                        np.angle(cell["dead"], deg=True)
                        - np.angle(cell["alive"], deg=True)
                    )
                    % 360
                )
            )
        case ColorMode.CONST:
            color_s = 100
        case _:
            print("not allowed")
    match color_mode_v:
        case ColorMode.A_MOD:
            color_v = int(100 * np.abs(cell["dead"]))
        case ColorMode.B_ABS:
            color_v = int(100 * np.abs(cell["alive"]))
        case ColorMode.A_PHASE:
            color_v = int((100.0 / 360.0) * (np.angle(cell["dead"], deg=True) % 360))
        case ColorMode.B_PHASE:
            color_v = int((100.0 / 360.0) * (np.angle(cell["alive"], deg=True) % 360))
        case ColorMode.DELTA_PHASE_BA:
            color_v = int(
                (100.0 / 360.0)
                * (
                    (
                        np.angle(cell["alive"], deg=True)
                        - np.angle(cell["dead"], deg=True)
                    )
                    % 360
                )
            )
        case ColorMode.DELTA_PHASE_AB:
            color_v = int(
                (100.0 / 360.0)
                * (
                    (
                        np.angle(cell["dead"], deg=True)
                        - np.angle(cell["alive"], deg=True)
                    )
                    % 360
                )
            )
        case ColorMode.CONST:
            color_v = 100
        case _:
            print("not allowed")
    color.hsva = (color_h, color_s, color_v, COLOR_ALPHA)
    return color


def get_color(
    cell,
    game_mode,
    color_mode_h: ColorMode,
    color_mode_s: ColorMode,
    color_mode_v: ColorMode,
):
    match game_mode:
        case GameMode.FUNCTIONAL:
            return color_functional(cell, color_mode_h, color_mode_s, color_mode_v)
        case GameMode.ENTANGLEMENT:
            return color_entangled(cell)
        case GameMode.HAMILTONIAN:
            return color_hamiltonian(cell)


def draw_grid(
    screen,
    game_mode,
    grid: np.ndarray,
    base: pygame.Vector2,
    scale,
    spacing,
    color_mode_h,
    color_mode_s,
    color_mode_v,
):
    drawn = np.zeros(np.shape(grid), dtype=pygame.Rect)
    for i, x in np.ndenumerate(grid):
        pos = (
            base
            + pygame.Vector2(i) * scale
            + pygame.Vector2(i).elementwise() * pygame.Vector2(spacing, spacing)
        )

        color = get_color(x, game_mode, color_mode_h, color_mode_s, color_mode_v)

        drawn[i] = pygame.draw.rect(
            screen,
            color,
            pygame.Rect(pos, (scale, scale)),
        )
    return drawn

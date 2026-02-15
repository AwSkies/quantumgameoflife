import numpy as np
import pygame

from .display_type import ColorMode

COLOR_ALPHA = 1.0


def color_entangled(cell):
    # TODO: Write function for calculating color in entangled mode
    color = pygame.Color(0, 0, 0)
    color.hsva = (0, 0, cell * 100, COLOR_ALPHA)
    return color


def color_unentangled(cell, color_mode_h, color_mode_s, color_mode_v):
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
            color_h = int(np.angle(cell["alive"] / cell["dead"], deg=True) % 360)
        case ColorMode.DELTA_PHASE_AB:
            color_h = int(np.angle(cell["dead"] / cell["alive"], deg=True) % 360)
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
                * (np.angle(cell["alive"] / cell["dead"], deg=True) % 360)
            )
        case ColorMode.DELTA_PHASE_AB:
            color_s = int(
                (100.0 / 360.0)
                * (np.angle(cell["dead"] / cell["alive"], deg=True) % 360)
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
                * (np.angle(cell["alive"] / cell["dead"], deg=True) % 360)
            )
        case ColorMode.DELTA_PHASE_AB:
            color_v = int(
                (100.0 / 360.0)
                * (np.angle(cell["dead"] / cell["alive"], deg=True) % 360)
            )
        case ColorMode.CONST:
            color_v = 100
        case _:
            print("not allowed")
    color.hsva = (color_h, color_s, color_v, COLOR_ALPHA)
    return color


def get_color(
    cell,
    mode,
    color_mode_h: ColorMode,
    color_mode_s: ColorMode,
    color_mode_v: ColorMode,
):
    if mode:
        return color_entangled(cell)
    else:
        return color_unentangled(cell, color_mode_h, color_mode_s, color_mode_v)


def draw_grid(
    screen,
    entanglement_mode,
    grid: np.ndarray,
    base: pygame.Vector2,
    scale,
    spacing,
    color_mode_h,
    color_mode_s,
    color_mode_v,
):
    for i, x in np.ndenumerate(grid):
        pos = (
            base
            + pygame.Vector2(i) * scale
            + pygame.Vector2(i).elementwise() * pygame.Vector2(spacing, spacing)
        )

        color = get_color(
            x, entanglement_mode, color_mode_h, color_mode_s, color_mode_v
        )

        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(pos, (scale, scale)),
        )

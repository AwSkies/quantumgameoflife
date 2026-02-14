import numpy as np
import pygame

from .display_type import DisplayType

COLOR_ALPHA = 1.0


def color_entangled(cell, mode, color_menu_h, color_menu_s, color_menu_l):
    # TODO: Write function for calculating color in entangled mode
    return 0


def color_unentangled(cell, mode, color_mode_h, color_mode_s, color_mode_v):
    color = pygame.Color(0, 0, 0)
    # Set defaults for if no mode is selected
    if color_mode_h == None:
        color_mode_h = DisplayType.phase_difference_ab
    if color_mode_s == None:
        color_mode_s = DisplayType.b_abs
    if color_mode_v == None:
        color_mode_v = DisplayType.b_abs
    color_h = 0
    color_s = 0
    color_v = 0
    match color_mode_h:
        case DisplayType.a_real:
            color_h = int(360 * cell["dead"].real)
        case DisplayType.b_real:
            color_h = int(360 * cell["alive"].real)
        case DisplayType.a_imag:
            color_h = int(360 * cell["dead"].imag)
        case DisplayType.b_imag:
            color_h = int(360 * cell["alive"].imag)
        case DisplayType.a_abs:
            color_h = int(360 * np.abs(cell["dead"]))
        case DisplayType.b_abs:
            color_h = int(360 * np.abs(cell["alive"]))
        case DisplayType.phase_a:
            color_h = int(np.angle(cell["dead"], deg=True) + 180)
        case DisplayType.phase_b:
            color_h = int(np.angle(cell["alive"], deg=True) + 180)
        case DisplayType.phase_difference_ba:
            color_h = int(np.angle(cell["alive"] / cell["dead"], deg=True) + 180)
        case DisplayType.phase_difference_ab:
            color_h = int(np.angle(cell["dead"] / cell["alive"], deg=True) + 180)
        case _:
            print("not allowed")
    match color_mode_s:
        case DisplayType.a_real:
            color_s = int(100 * cell["dead"].real)
        case DisplayType.b_real:
            color_s = int(100 * cell["alive"].real)
        case DisplayType.a_imag:
            color_s = int(100 * cell["dead"].imag)
        case DisplayType.b_imag:
            color_s = int(100 * cell["alive"].imag)
        case DisplayType.a_abs:
            color_s = int(100 * np.abs(cell["dead"]))
        case DisplayType.b_abs:
            color_s = int(100 * np.abs(cell["alive"]))
        case DisplayType.phase_a:
            color_s = int((100.0 / 360.0) * (np.angle(cell["dead"], deg=True) + 180))
        case DisplayType.phase_b:
            color_s = int((100.0 / 360.0) * (np.angle(cell["alive"], deg=True) + 180))
        case DisplayType.phase_difference_ba:
            color_s = int(
                (100.0 / 360.0)
                * (np.angle(cell["alive"] / cell["dead"], deg=True) + 180)
            )
        case DisplayType.phase_difference_ab:
            color_s = int(
                (100.0 / 360.0)
                * (np.angle(cell["dead"] / cell["alive"], deg=True) + 180)
            )
        case _:
            print("not allowed")
    match color_mode_v:
        case DisplayType.a_real:
            color_v = int(100 * cell["dead"].real)
        case DisplayType.b_real:
            color_v = int(100 * cell["alive"].real)
        case DisplayType.a_imag:
            color_v = int(100 * cell["dead"].imag)
        case DisplayType.b_imag:
            color_v = int(100 * cell["alive"].imag)
        case DisplayType.a_abs:
            color_v = int(100 * np.abs(cell["dead"]))
        case DisplayType.b_abs:
            color_v = int(100 * np.abs(cell["alive"]))
        case DisplayType.phase_a:
            color_v = int((100.0 / 360.0) * (np.angle(cell["dead"], deg=True) + 180))
        case DisplayType.phase_b:
            color_v = int((100.0 / 360.0) * (np.angle(cell["alive"], deg=True) + 180))
        case DisplayType.phase_difference_ba:
            color_v = int(
                (100.0 / 360.0)
                * (np.angle(cell["alive"] / cell["dead"], deg=True) + 180)
            )
        case DisplayType.phase_difference_ab:
            color_v = int(
                (100.0 / 360.0)
                * (np.angle(cell["dead"] / cell["alive"], deg=True) + 180)
            )
        case _:
            print("not allowed")
    color.hsva = (color_h, color_s, color_v, COLOR_ALPHA)
    return color


def get_color(
    cell,
    mode,
    color_mode_h: DisplayType,
    color_mode_s: DisplayType,
    color_mode_v: DisplayType,
):
    if mode:
        return color_entangled(cell, mode, color_mode_h, color_mode_s, color_mode_v)
    else:
        return color_unentangled(cell, mode, color_mode_h, color_mode_s, color_mode_v)


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

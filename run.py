import pygame
import pygame_widgets
import numpy as np
from pygame_widgets.slider import Slider
from quantumgameoflife import cells
from quantumgameoflife import DisplayType

RES_X = 1280
RES_Y = 720

SLIDER_OFFSET = 100
SLIDER_HEIGHT = 50
SLIDER_WIDTH = RES_X // 4

PAN_SPEED = 10
ZOOM_SPEED = 0.5
SCALE_MIN = 1
SCALE_MAX = 10
N_CELLS_X = 10
N_CELLS_Y = 20
CELL_SIZE = 10
SPACING = 0.5  # spacing between cells in fraction of full cell size
COLOR_ALPHA = 1.0 

def color_option(cell, color_menu_h: DisplayType, color_menu_s: DisplayType, color_menu_v: DisplayType):
    color = pygame.Color(0,0,0)
    color.hsla = (0.0, 0.0, 0.0, COLOR_ALPHA)
    match color_menu_h:
        case 'real part of a':
            print(color_menu_h)
            print(cell['dead'])
        case _:
            print('not allowed')
    match color_menu_s:
        case 'real part of a':
            print(color_menu_s)
        case _:
            print('not allowed')
    match color_menu_v:
        case 'real part of a':
            print(color_menu_v)
        case _:
            print('not allowed')
    return color 

def draw_grid(screen, entanglement_mode, grid: np.ndarray, base: pygame.Vector2, scale, spacing):
    for i, x in np.ndenumerate(grid):
        pos = (
            base
            + pygame.Vector2(i) * scale
            + pygame.Vector2(i).elementwise() * pygame.Vector2(spacing, spacing)
        )
        # TODO: Interpret color properly
        color_H = int(360 * ((x + np.pi) / (2 * np.pi)))
        color_S = int(100 * x)
        color_L = int(100 * x)
        color_A = 100
        color = pygame.Color(0,0,0)
        color.hsla = (color_H, color_S, color_L, color_A)
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(pos, (scale, scale)),
        )


def main():
    pygame.init()
    screen = pygame.display.set_mode((RES_X, RES_Y))
    clock = pygame.time.Clock()

    speed_slider = Slider(screen, RES_X // 2 - SLIDER_WIDTH // 2, RES_Y - SLIDER_OFFSET, SLIDER_WIDTH, SLIDER_HEIGHT, min=0, max=100, step=1)

    running = True
    entanglement_mode = False
    pan = pygame.Vector2()
    scale = 1.0

    # TODO: Initialize grid properly

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEWHEEL:
                # Zoom instead of pan when CTRL is held
                mod_keys = pygame.key.get_mods()
                if mod_keys & (pygame.KMOD_RCTRL | pygame.KMOD_LCTRL):
                    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

                    # World position before zoom
                    world_pos = (mouse_pos - pan) / scale

                    # Apply zoom
                    new_scale = pygame.math.clamp(
                        scale + event.y * ZOOM_SPEED, SCALE_MIN, SCALE_MAX
                    )

                    # Adjust pan so the world point under cursor stays fixed
                    pan = mouse_pos - world_pos * new_scale

                    scale = new_scale
                elif (
                    mod_keys & (pygame.KMOD_LSHIFT | pygame.KMOD_RSHIFT)
                    and not event.touch
                ):
                    pan += pygame.Vector2(event.y, 0) * PAN_SPEED
                else:
                    pan += pygame.Vector2(event.x, event.y) * PAN_SPEED

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # TODO: Perform grid operations
        x = np.linspace(0.0, 0.5, N_CELLS_X)
        y = np.linspace(0.0, 0.5, N_CELLS_Y)
        y = y.reshape((N_CELLS_Y, 1))
        grid = x + y

        draw_grid(
            screen,
            entanglement_mode,
            grid.transpose(),
            pan,
            CELL_SIZE * scale,
            CELL_SIZE * SPACING * scale,
        )

        pygame_widgets.update(events)
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == "__main__":
    #main()
    cells_matrix = cells.make_cell_array(2, 2)
    cells.random_initialize(cells_matrix)
    color_menu_h = DisplayType.a_real
    color_menu_s = DisplayType.b_img
    color_menu_v = DisplayType.b_real
    color_option(cells_matrix[0][0], color_menu_h, color_menu_s, color_menu_v)
    #print(DisplayType.a_img)

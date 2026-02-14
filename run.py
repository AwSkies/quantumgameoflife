import pygame
import pygame_widgets
import numpy as np
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from pygame_widgets.toggle import Toggle
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown

RES_X = 1280
RES_Y = 720

SLIDER_OFFSET = 100
SLIDER_HEIGHT = 50
SLIDER_WIDTH = RES_X // 4
SLIDER_X = RES_X // 2 - SLIDER_WIDTH // 2

OBSERVE_BUTTON_OFFSET_X = 100
OBSERVE_BUTTON_OFFSET_Y = 50
OBSERVE_BUTTON_HEIGHT = 100
OBSERVE_BUTTON_WIDTH = 200
OBSERVE_BUTTON_RADIUS = 25

PLAY_TOGGLE_OFFSET_X = 100
PLAY_TOGGLE_OFFSET_Y = 50
PLAY_TOGGLE_HEIGHT = 25
PLAY_TOGGLE_WIDTH = 50

MODE_TOGGLE_OFFSET_X = 50
MODE_TOGGLE_OFFSET_Y = 50
MODE_TOGGLE_HEIGHT = 25
MODE_TOGGLE_WIDTH = 50
MODE_TOGGLE_RADIUS = 25
MODE_TOGGLE_X = RES_X - MODE_TOGGLE_OFFSET_X - MODE_TOGGLE_WIDTH
MODE_TOGGLE_Y = MODE_TOGGLE_OFFSET_Y

STEP_COUNTER_OFFSET_X = 10
STEP_COUNTER_OFFSET_Y = 10
STEP_COUNTER_HEIGHT = 50
STEP_COUNTER_WIDTH = 50
STEP_COUNTER_RADIUS = 10

HSV_DROPDOWNS_OFFSET_X = 25
HSV_DROPDOWNS_OFFSET_Y = 15
HSV_DROPDOWNS_HEIGHT = 50
HSV_DROPDOWNS_WIDTH = 100
HSV_DROPDOWNS_RADIUS = 10
HSV_DROPDOWNS_X = RES_X - HSV_DROPDOWNS_WIDTH - HSV_DROPDOWNS_OFFSET_X

# TODO: Make actual list of color options
COLOR_OPTIONS = list(['a', 'b', 'c'])

PAN_SPEED = 10
ZOOM_SPEED = 0.5
SCALE_MIN = 1
SCALE_MAX = 10
N_CELLS_X = 10
N_CELLS_Y = 20
CELL_SIZE = 10
SPACING = 0.5  # spacing between cells in fraction of full cell size
SIMULATION_SPEED = 1


def draw_grid(screen, entanglement_mode, grid: np.ndarray, base: pygame.Vector2, scale, spacing):
    for i, x in np.ndenumerate(grid):
        pos = (
            base
            + pygame.Vector2(i) * scale
            + pygame.Vector2(i).elementwise() * pygame.Vector2(spacing, spacing)
        )
        # TODO: Interpret color properly
        color = int(255 * x)
        pygame.draw.rect(
            screen,
            pygame.Color(color, color, color),
            pygame.Rect(pos, (scale, scale)),
        )


def main():
    pygame.init()
    screen = pygame.display.set_mode((RES_X, RES_Y))
    clock = pygame.time.Clock()

    running = True
    entanglement_mode = False
    pan = pygame.Vector2()
    scale = 1.0
    step = 0

    # TODO: Initialize grid properly
    x = np.linspace(0.0, 0.5, N_CELLS_X)
    y = np.linspace(0.0, 0.5, N_CELLS_Y)
    y = y.reshape((N_CELLS_Y, 1))
    grid = x + y

    def observe():
        nonlocal grid
        # TODO: Perform actual observation calculation
        grid = np.ones((N_CELLS_Y, N_CELLS_X))

    speed_slider = Slider(
        screen,
        SLIDER_X,
        RES_Y - SLIDER_OFFSET,
        SLIDER_WIDTH,
        SLIDER_HEIGHT,
        min=0,
        max=100,
        step=1,
    )
    observe_button = Button(
        screen,
        SLIDER_X - OBSERVE_BUTTON_WIDTH - OBSERVE_BUTTON_OFFSET_X,
        RES_Y - OBSERVE_BUTTON_HEIGHT - OBSERVE_BUTTON_OFFSET_Y,
        OBSERVE_BUTTON_WIDTH,
        OBSERVE_BUTTON_HEIGHT,
        radius=OBSERVE_BUTTON_RADIUS,
        onClick=observe,
        text="Observe",
    )
    play_toggle = Toggle(
        screen,
        SLIDER_X + SLIDER_WIDTH + PLAY_TOGGLE_OFFSET_X,
        RES_Y - PLAY_TOGGLE_HEIGHT - PLAY_TOGGLE_OFFSET_Y,
        PLAY_TOGGLE_WIDTH,
        PLAY_TOGGLE_HEIGHT,
        startOn=True
    )
    mode_toggle = Toggle(
        screen,
        MODE_TOGGLE_X,
        MODE_TOGGLE_Y,
        MODE_TOGGLE_WIDTH, 
        MODE_TOGGLE_HEIGHT,
        startOn=entanglement_mode
    )
    h_dropdown = Dropdown(
        screen,
        HSV_DROPDOWNS_X,
        MODE_TOGGLE_Y + MODE_TOGGLE_HEIGHT + HSV_DROPDOWNS_OFFSET_Y,
        HSV_DROPDOWNS_WIDTH,
        HSV_DROPDOWNS_HEIGHT,
        'Hue',
        COLOR_OPTIONS,
        radius=HSV_DROPDOWNS_RADIUS
    )
    s_dropdown = Dropdown(
        screen,
        HSV_DROPDOWNS_X,
        MODE_TOGGLE_Y + MODE_TOGGLE_HEIGHT + 2 * HSV_DROPDOWNS_OFFSET_Y + HSV_DROPDOWNS_HEIGHT,
        HSV_DROPDOWNS_WIDTH,
        HSV_DROPDOWNS_HEIGHT,
        'Saturation',
        COLOR_OPTIONS,
        radius=HSV_DROPDOWNS_RADIUS
    )
    l_dropdown = Dropdown(
        screen,
        HSV_DROPDOWNS_X,
        MODE_TOGGLE_Y + MODE_TOGGLE_HEIGHT + 3 * HSV_DROPDOWNS_OFFSET_Y + 2 * HSV_DROPDOWNS_HEIGHT,
        HSV_DROPDOWNS_WIDTH,
        HSV_DROPDOWNS_HEIGHT,
        'Lightness',
        COLOR_OPTIONS,
        radius=HSV_DROPDOWNS_RADIUS
    )
    # TODO: Make text boxes on either side of the mode toggle to indicate freeform or entanglement mode
    step_counter = TextBox(
        screen,
        STEP_COUNTER_OFFSET_X,
        STEP_COUNTER_OFFSET_Y,
        STEP_COUNTER_WIDTH,
        STEP_COUNTER_HEIGHT,
        radius=STEP_COUNTER_RADIUS
    )
    step_counter.disable()

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

        entanglement_mode = mode_toggle.getValue()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # TODO: Perform grid operations

        draw_grid(
            screen,
            entanglement_mode,
            grid.transpose(),
            pan,
            CELL_SIZE * scale,
            CELL_SIZE * SPACING * scale,
        )

        for dropdown in [l_dropdown, s_dropdown, h_dropdown]:
            if entanglement_mode:
                dropdown.show()
            else:
                dropdown.hide()

        step_counter.setText(str(step))
        
        # TODO: Do step calculations based on `speed_slider.getValue()` and `SIMULATION_SPEED`. Maybe count the nunber of frames passed.
        if play_toggle.getValue():
            step += 1

        pygame_widgets.update(events)
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == "__main__":
    main()

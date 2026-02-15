import pygame
import pygame_widgets
import numpy as np
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from pygame_widgets.toggle import Toggle
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown
from quantumgameoflife import functional_cells
from quantumgameoflife import entanglement_cells
from quantumgameoflife import ColorMode
from quantumgameoflife import draw_grid

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

FUNCTIONAL_OPTIONS_OFFSET_X = 25
FUNCTIONAL_OPTIONS_OFFSET_Y = 15
FUNCTIONAL_OPTIONS_HEIGHT = 50
FUNCTIONAL_OPTIONS_WIDTH = 100
FUNCTIONAL_OPTIONS_RADIUS = 10
FUNCTIONAL_OPTIONS_X = RES_X - FUNCTIONAL_OPTIONS_WIDTH - FUNCTIONAL_OPTIONS_OFFSET_X

COLOR_OPTIONS = list(ColorMode)

PAN_SPEED = 10
ZOOM_SPEED = 0.5
SCALE_MIN = 1
SCALE_MAX = 10
N_CELLS_X = 30
N_CELLS_Y = 30
CELL_SIZE = 10
SPACING = 0.5  # spacing between cells in fraction of full cell size
SIMULATION_STEP_FRAMES = 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((RES_X, RES_Y))
    clock = pygame.time.Clock()

    running = True
    entanglement_mode = False
    pan = pygame.Vector2()
    scale = 1.0
    step = 0
    step_frames = 0
    grid_drawn = np.zeros((RES_X, RES_Y), dtype=pygame.Rect)
    cell_selected = (0, 0)

    entangled_lattice = entanglement_cells.Lattice(N_CELLS_X, N_CELLS_Y)
    functional_lattice = functional_cells.Lattice(N_CELLS_X, N_CELLS_Y)

    def observe():
        # TODO: Perform actual observation calculation on the correct lattice object depending on the mode
        ...

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
        startOn=False,
    )
    mode_toggle = Toggle(
        screen,
        MODE_TOGGLE_X,
        MODE_TOGGLE_Y,
        MODE_TOGGLE_WIDTH,
        MODE_TOGGLE_HEIGHT,
        startOn=entanglement_mode,
    )
    h_dropdown = Dropdown(
        screen,
        FUNCTIONAL_OPTIONS_X,
        MODE_TOGGLE_Y + MODE_TOGGLE_HEIGHT + FUNCTIONAL_OPTIONS_OFFSET_Y,
        FUNCTIONAL_OPTIONS_WIDTH,
        FUNCTIONAL_OPTIONS_HEIGHT,
        "Hue",
        COLOR_OPTIONS,
        radius=FUNCTIONAL_OPTIONS_RADIUS,
    )
    s_dropdown = Dropdown(
        screen,
        FUNCTIONAL_OPTIONS_X,
        MODE_TOGGLE_Y
        + MODE_TOGGLE_HEIGHT
        + 2 * FUNCTIONAL_OPTIONS_OFFSET_Y
        + FUNCTIONAL_OPTIONS_HEIGHT,
        FUNCTIONAL_OPTIONS_WIDTH,
        FUNCTIONAL_OPTIONS_HEIGHT,
        "Saturation",
        COLOR_OPTIONS,
        radius=FUNCTIONAL_OPTIONS_RADIUS,
    )
    v_dropdown = Dropdown(
        screen,
        FUNCTIONAL_OPTIONS_X,
        MODE_TOGGLE_Y
        + MODE_TOGGLE_HEIGHT
        + 3 * FUNCTIONAL_OPTIONS_OFFSET_Y
        + 2 * FUNCTIONAL_OPTIONS_HEIGHT,
        FUNCTIONAL_OPTIONS_WIDTH,
        FUNCTIONAL_OPTIONS_HEIGHT,
        "Value",
        COLOR_OPTIONS,
        radius=FUNCTIONAL_OPTIONS_RADIUS,
    )
    function_dropdown = Dropdown(
        screen,
        FUNCTIONAL_OPTIONS_X,
        MODE_TOGGLE_Y
        + MODE_TOGGLE_HEIGHT
        + 4 * FUNCTIONAL_OPTIONS_OFFSET_Y
        + 3 * FUNCTIONAL_OPTIONS_HEIGHT,
        FUNCTIONAL_OPTIONS_WIDTH,
        FUNCTIONAL_OPTIONS_HEIGHT,
        "Function",
        list(functional_cells.Functions),
        radius=FUNCTIONAL_OPTIONS_RADIUS,
    )
    alive_slider = Slider(
        screen,
        FUNCTIONAL_OPTIONS_X,
        MODE_TOGGLE_Y
        + MODE_TOGGLE_HEIGHT
        + 5 * FUNCTIONAL_OPTIONS_OFFSET_Y
        + 4 * FUNCTIONAL_OPTIONS_HEIGHT,
        FUNCTIONAL_OPTIONS_WIDTH,
        FUNCTIONAL_OPTIONS_HEIGHT,
        min=0,
        max=100,
        step=1,
    )
    phase1_slider = Slider(
        screen,
        FUNCTIONAL_OPTIONS_X,
        MODE_TOGGLE_Y
        + MODE_TOGGLE_HEIGHT
        + 6 * FUNCTIONAL_OPTIONS_OFFSET_Y
        + 5 * FUNCTIONAL_OPTIONS_HEIGHT,
        FUNCTIONAL_OPTIONS_WIDTH,
        FUNCTIONAL_OPTIONS_HEIGHT,
        min=0,
        max=359,
        step=1,
    )
    phase2_slider = Slider(
        screen,
        FUNCTIONAL_OPTIONS_X,
        MODE_TOGGLE_Y
        + MODE_TOGGLE_HEIGHT
        + 7 * FUNCTIONAL_OPTIONS_OFFSET_Y
        + 6 * FUNCTIONAL_OPTIONS_HEIGHT,
        FUNCTIONAL_OPTIONS_WIDTH,
        FUNCTIONAL_OPTIONS_HEIGHT,
        min=0,
        max=359,
        step=1,
    )
    # TODO: Make text boxes on either side of the mode toggle to indicate freeform or entanglement mode
    step_counter = TextBox(
        screen,
        STEP_COUNTER_OFFSET_X,
        STEP_COUNTER_OFFSET_Y,
        STEP_COUNTER_WIDTH,
        STEP_COUNTER_HEIGHT,
        radius=STEP_COUNTER_RADIUS,
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
                    pan += pygame.Vector2(event.x, -event.y) * PAN_SPEED

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Get which cell has been clicked on (if any)
                    pos = pygame.mouse.get_pos()
                    clicked = False
                    for i, r in np.ndenumerate(grid_drawn):
                        if r.collidepoint(pos):
                            cell_selected = i
                            clicked = True
                    if clicked:
                        # Update sliders
                        if not entanglement_mode:
                            c = functional_lattice.grid[cell_selected]
                            alive_slider.setValue(int(np.square(np.abs(c["alive"])) * 100))
                            phase1_slider.setValue(int(np.angle(c["dead"], deg=True)))
                            phase2_slider.setValue(int(np.angle(c["alive"], deg=True)))

        entanglement_mode = mode_toggle.getValue()

        if step_frames > SIMULATION_STEP_FRAMES * (1 - (speed_slider.getValue() / 100)):
            step += 1
            if entanglement_mode:
                entangled_lattice.step()
            else:
                functional_lattice.step()
            step_frames = 0

        functional_lattice.set_function(function_dropdown.getSelected())

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # Set the selected cell's values

        if not entanglement_mode:
            r_alive = np.sqrt(alive_slider.getValue() / 100.0)
            phase1 = 2j * np.pi * phase1_slider.getValue() / 360
            phase2 = 2j * np.pi * phase2_slider.getValue() / 360
            functional_cells.set_cell_value(
                functional_lattice.grid[cell_selected],
                np.sqrt(1 - np.square(r_alive)) * np.exp(phase1),
                r_alive * np.exp(phase2),
            )

        if entanglement_mode:
            grid = entangled_lattice.alive_magnitudes
        else:
            grid = functional_lattice.grid

        grid_drawn = draw_grid(
            screen,
            entanglement_mode,
            grid,
            pan,
            CELL_SIZE * scale,
            CELL_SIZE * SPACING * scale,
            h_dropdown.getSelected(),
            s_dropdown.getSelected(),
            v_dropdown.getSelected(),
        )

        for component in [
            phase2_slider,
            phase1_slider,
            alive_slider,
            function_dropdown,
            v_dropdown,
            s_dropdown,
            h_dropdown,
        ]:
            if entanglement_mode:
                component.hide()
            else:
                component.show()

        step_counter.setText(str(step))

        if play_toggle.getValue():
            step_frames += 1

        pygame_widgets.update(events)
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == "__main__":
    main()

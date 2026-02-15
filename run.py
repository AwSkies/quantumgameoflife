import pygame
import pygame_widgets
import numpy as np
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from pygame_widgets.toggle import Toggle
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown
from quantumgameoflife import functional
from quantumgameoflife import hamiltonian
from quantumgameoflife import entanglement
from quantumgameoflife import ColorMode
from quantumgameoflife import GameMode
from quantumgameoflife import draw_grid

RES_X = 1664
RES_Y = 936

SLIDER_HANDLE_COLOR = (66, 135, 245)

SLIDER_OFFSET = 100
SLIDER_HEIGHT = 50
SLIDER_WIDTH = RES_X // 4
SLIDER_X = RES_X // 2 - SLIDER_WIDTH // 2

OBSERVE_BUTTON_OFFSET_X = 100
OBSERVE_BUTTON_OFFSET_Y = 25
OBSERVE_BUTTON_HEIGHT = 100
OBSERVE_BUTTON_WIDTH = 200
OBSERVE_BUTTON_RADIUS = 25

PLAY_TOGGLE_OFFSET_X = 100
PLAY_TOGGLE_OFFSET_Y = 60
PLAY_TOGGLE_HEIGHT = 25
PLAY_TOGGLE_WIDTH = 50

STEP_COUNTER_OFFSET_X = 10
STEP_COUNTER_OFFSET_Y = 10
STEP_COUNTER_HEIGHT = 35
STEP_COUNTER_WIDTH = 75
STEP_COUNTER_RADIUS = 5

MODE_OPTIONS_OFFSET_X = 25
MODE_OPTIONS_OFFSET_Y = 15
MODE_OPTIONS_HEIGHT = 50
MODE_OPTIONS_WIDTH = 100
MODE_OPTIONS_RADIUS = 10
MODE_OPTIONS_X = RES_X - MODE_OPTIONS_WIDTH - MODE_OPTIONS_OFFSET_X
PHASE_TOGGLE_WIDTH = 50
PHASE_TOGGLE_HEIGHT = 25
PHASE_TOGGLE_OFFSET_X = 15

EDITOR_OPTIONS_OFFSET_X = 25
EDITOR_OPTIONS_OFFSET_Y = 25
EDITOR_OPTIONS_HEIGHT = 30
EDITOR_OPTIONS_WIDTH = 100
EDITOR_RIGHT_CAPTION_WIDTH = 50
EDITOR_LEFT_CAPTION_WIDTH = 50
EDITOR_LABEL_WIDTH = 80
EDITOR_CAPTION_HEIGHT = 35
EDITOR_RIGHT_CAPTION_X = RES_X - EDITOR_OPTIONS_OFFSET_X - EDITOR_RIGHT_CAPTION_WIDTH
EDITOR_OPTIONS_X = (
    EDITOR_RIGHT_CAPTION_X - EDITOR_OPTIONS_WIDTH - EDITOR_OPTIONS_OFFSET_X
)
EDITOR_LEFT_CAPTION_X = (
    EDITOR_OPTIONS_X - EDITOR_LEFT_CAPTION_WIDTH - EDITOR_OPTIONS_OFFSET_X
)
EDITOR_LABEL_X = EDITOR_LEFT_CAPTION_X - EDITOR_LABEL_WIDTH - EDITOR_OPTIONS_OFFSET_X

COLOR_OPTIONS = list(ColorMode)

PAN_SPEED = 10
ZOOM_SPEED = 0.5
SCALE_MIN = 1
SCALE_MAX = 10
N_CELLS_X = 35
N_CELLS_Y = 35
CELL_SIZE = 10
SPACING = 0.5  # spacing between cells in fraction of full cell size
SIMULATION_STEP_FRAMES = 60


def update_editor_values(
    grid, qubits, cell_selected, alive_slider, phase1_slider, phase2_slider
):
    if qubits:
        c = grid[cell_selected]
        alive_slider.setValue(int(np.square(np.abs(c["alive"])) * 100))
        phase1_slider.setValue(int(np.angle(c["dead"], deg=True) % 360))
        phase2_slider.setValue(int(np.angle(c["alive"], deg=True) % 360))


def main():
    pygame.init()
    screen = pygame.display.set_mode((RES_X, RES_Y))
    clock = pygame.time.Clock()

    running = True
    game_mode = GameMode.FUNCTIONAL
    qubits = True
    entanglement_presets = list(entanglement.Preset)
    scale = 1.0

    # Initialize pan such that the grid is centered
    STEP = CELL_SIZE * (1 + SPACING)
    grid_width = (N_CELLS_X - 1) * STEP + CELL_SIZE
    grid_height = (N_CELLS_Y - 1) * STEP + CELL_SIZE
    world_center = pygame.Vector2(grid_width / 2, grid_height / 2)
    screen_center = pygame.Vector2(RES_X // 2, RES_Y // 2)
    pan = screen_center - world_center * scale

    step = 0
    step_frames = 0
    grid_drawn = np.zeros((RES_X, RES_Y), dtype=pygame.Rect)
    cell_selected = (0, 0)

    entangled_lattice = entanglement.Lattice(N_CELLS_X, N_CELLS_Y)
    functional_lattice = functional.Lattice(N_CELLS_X, N_CELLS_Y)
    hamiltonian_lattice = hamiltonian.Lattice(N_CELLS_X, N_CELLS_Y)

    def observe():
        if game_mode == GameMode.FUNCTIONAL:
            functional_lattice.observe()

    speed_slider = Slider(
        screen,
        SLIDER_X,
        RES_Y - SLIDER_OFFSET,
        SLIDER_WIDTH,
        SLIDER_HEIGHT,
        min=0,
        max=100,
        step=1,
        initial=0,
        handleColour=SLIDER_HANDLE_COLOR,
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
    mode_dropdown = Dropdown(
        screen,
        MODE_OPTIONS_X,
        MODE_OPTIONS_OFFSET_Y,
        MODE_OPTIONS_WIDTH,
        MODE_OPTIONS_HEIGHT,
        "Game mode",
        list(GameMode),
    )
    h_dropdown = Dropdown(
        screen,
        MODE_OPTIONS_X,
        MODE_OPTIONS_HEIGHT + 2 * MODE_OPTIONS_OFFSET_Y,
        MODE_OPTIONS_WIDTH,
        MODE_OPTIONS_HEIGHT,
        "Hue",
        COLOR_OPTIONS,
        radius=MODE_OPTIONS_RADIUS,
    )
    s_dropdown = Dropdown(
        screen,
        MODE_OPTIONS_X,
        2 * MODE_OPTIONS_HEIGHT + 3 * MODE_OPTIONS_OFFSET_Y,
        MODE_OPTIONS_WIDTH,
        MODE_OPTIONS_HEIGHT,
        "Saturation",
        COLOR_OPTIONS,
        radius=MODE_OPTIONS_RADIUS,
    )
    v_dropdown = Dropdown(
        screen,
        MODE_OPTIONS_X,
        3 * MODE_OPTIONS_HEIGHT + 4 * MODE_OPTIONS_OFFSET_Y,
        MODE_OPTIONS_WIDTH,
        MODE_OPTIONS_HEIGHT,
        "Value",
        COLOR_OPTIONS,
        radius=MODE_OPTIONS_RADIUS,
    )
    function_dropdown = Dropdown(
        screen,
        MODE_OPTIONS_X,
        4 * MODE_OPTIONS_HEIGHT + 5 * MODE_OPTIONS_OFFSET_Y,
        MODE_OPTIONS_WIDTH,
        MODE_OPTIONS_HEIGHT,
        "Function",
        list(functional.Functions),
        radius=MODE_OPTIONS_RADIUS,
    )
    phase_toggle = Toggle(
        screen,
        MODE_OPTIONS_X + PHASE_TOGGLE_OFFSET_X,
        MODE_OPTIONS_HEIGHT + 2 * MODE_OPTIONS_OFFSET_Y,
        PHASE_TOGGLE_WIDTH,
        PHASE_TOGGLE_HEIGHT,
        startOn=False,
    )
    preset_dropdown = Dropdown(
        screen,
        MODE_OPTIONS_X,
        MODE_OPTIONS_HEIGHT + 2 * MODE_OPTIONS_OFFSET_Y,
        MODE_OPTIONS_WIDTH,
        MODE_OPTIONS_HEIGHT,
        "Preset",
        entanglement_presets,
        radius=MODE_OPTIONS_RADIUS,
    )
    preset_button = Button(
        screen,
        MODE_OPTIONS_X,
        2 * MODE_OPTIONS_HEIGHT + 3 * MODE_OPTIONS_OFFSET_Y,
        MODE_OPTIONS_WIDTH,
        MODE_OPTIONS_HEIGHT,
        radius=MODE_OPTIONS_RADIUS,
        onClick=lambda: entangled_lattice.set_to_preset(
            entanglement_presets.index(
                entanglement.Preset(preset_dropdown.getSelected())
            )
            if preset_dropdown.getSelected() != None
            else 0
        ),
        text="Set to preset",
    )
    ALIVE_Y = RES_Y - 3 * EDITOR_OPTIONS_OFFSET_Y - 3 * EDITOR_OPTIONS_HEIGHT
    alive_slider = Slider(
        screen,
        EDITOR_OPTIONS_X,
        ALIVE_Y,
        EDITOR_OPTIONS_WIDTH,
        EDITOR_OPTIONS_HEIGHT,
        min=0,
        max=100,
        step=1,
        initial=100,
        handleColour=SLIDER_HANDLE_COLOR,
    )
    alive_right_caption = TextBox(
        screen,
        EDITOR_RIGHT_CAPTION_X,
        ALIVE_Y,
        EDITOR_RIGHT_CAPTION_WIDTH,
        EDITOR_CAPTION_HEIGHT,
    )
    alive_right_caption.setText("1")
    alive_left_caption = TextBox(
        screen,
        EDITOR_LEFT_CAPTION_X,
        ALIVE_Y,
        EDITOR_LEFT_CAPTION_WIDTH,
        EDITOR_CAPTION_HEIGHT,
    )
    alive_left_caption.setText("0")
    alive_label = TextBox(
        screen,
        EDITOR_LABEL_X,
        ALIVE_Y,
        EDITOR_LABEL_WIDTH,
        EDITOR_CAPTION_HEIGHT,
    )
    alive_label.setText("|b|:")
    PHASE1_Y = RES_Y - 2 * EDITOR_OPTIONS_OFFSET_Y - 2 * EDITOR_OPTIONS_HEIGHT
    phase1_slider = Slider(
        screen,
        EDITOR_OPTIONS_X,
        PHASE1_Y,
        EDITOR_OPTIONS_WIDTH,
        EDITOR_OPTIONS_HEIGHT,
        min=0,
        max=359,
        step=1,
        initial=0,
        handleColour=SLIDER_HANDLE_COLOR,
    )
    phase1_right_caption = TextBox(
        screen,
        EDITOR_RIGHT_CAPTION_X,
        PHASE1_Y,
        EDITOR_RIGHT_CAPTION_WIDTH,
        EDITOR_CAPTION_HEIGHT,
    )
    phase1_right_caption.setText("360")
    phase1_left_caption = TextBox(
        screen,
        EDITOR_LEFT_CAPTION_X,
        PHASE1_Y,
        EDITOR_LEFT_CAPTION_WIDTH,
        EDITOR_CAPTION_HEIGHT,
    )
    phase1_left_caption.setText("0")
    phase1_label = TextBox(
        screen,
        EDITOR_LABEL_X,
        PHASE1_Y,
        EDITOR_LABEL_WIDTH,
        EDITOR_CAPTION_HEIGHT,
    )
    phase1_label.setText("arg(a):")
    PHASE2_Y = RES_Y - EDITOR_OPTIONS_OFFSET_Y - EDITOR_OPTIONS_HEIGHT
    phase2_slider = Slider(
        screen,
        EDITOR_OPTIONS_X,
        PHASE2_Y,
        EDITOR_OPTIONS_WIDTH,
        EDITOR_OPTIONS_HEIGHT,
        min=0,
        max=359,
        step=1,
        initial=0,
        handleColour=SLIDER_HANDLE_COLOR,
    )
    phase2_right_caption = TextBox(
        screen,
        EDITOR_RIGHT_CAPTION_X,
        PHASE2_Y,
        EDITOR_RIGHT_CAPTION_WIDTH,
        EDITOR_CAPTION_HEIGHT,
    )
    phase2_right_caption.setText("360")
    phase2_left_caption = TextBox(
        screen,
        EDITOR_LEFT_CAPTION_X,
        PHASE2_Y,
        EDITOR_LEFT_CAPTION_WIDTH,
        EDITOR_CAPTION_HEIGHT,
    )
    phase2_left_caption.setText("0")
    phase2_label = TextBox(
        screen,
        EDITOR_LABEL_X,
        PHASE2_Y,
        EDITOR_LABEL_WIDTH,
        EDITOR_CAPTION_HEIGHT,
    )
    phase2_label.setText("arg(b):")
    step_counter = TextBox(
        screen,
        STEP_COUNTER_OFFSET_X,
        STEP_COUNTER_OFFSET_Y,
        STEP_COUNTER_WIDTH,
        STEP_COUNTER_HEIGHT,
        radius=STEP_COUNTER_RADIUS,
    )
    for text_box in [
        step_counter,
        alive_left_caption,
        alive_right_caption,
        alive_label,
        phase1_left_caption,
        phase1_right_caption,
        phase1_label,
        phase2_left_caption,
        phase2_right_caption,
        phase2_label,
    ]:
        text_box.disable()
    # TODO: Make labels

    while running:
        game_mode = mode_dropdown.getSelected()
        if game_mode == None:
            game_mode = GameMode.FUNCTIONAL
        qubits = game_mode == GameMode.FUNCTIONAL or game_mode == GameMode.HAMILTONIAN

        match game_mode:
            case GameMode.FUNCTIONAL:
                editable_grid = functional_lattice.grid
            case GameMode.HAMILTONIAN:
                editable_grid = hamiltonian_lattice.grid

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
                    if clicked and qubits:
                        # Update sliders
                        update_editor_values(
                            editable_grid,
                            qubits,
                            cell_selected,
                            alive_slider,
                            phase1_slider,
                            phase2_slider,
                        )

        if step_frames > SIMULATION_STEP_FRAMES * (1 - (speed_slider.getValue() / 100)):
            step += 1
            step_frames = 0
            match game_mode:
                case GameMode.FUNCTIONAL:
                    functional_lattice.step()
                case GameMode.ENTANGLEMENT:
                    entangled_lattice.step()
                case GameMode.HAMILTONIAN:
                    hamiltonian_lattice.step(phase_toggle.getValue())

        functional_lattice.set_function(function_dropdown.getSelected())

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # Set the selected cell's values
        if qubits:
            if not play_toggle.getValue():
                r_alive = np.sqrt(alive_slider.getValue() / 100.0)
                phase1 = 2j * np.pi * phase1_slider.getValue() / 360
                phase2 = 2j * np.pi * phase2_slider.getValue() / 360
                functional.set_cell_value(
                    editable_grid[cell_selected],
                    np.sqrt(1 - np.square(r_alive)) * np.exp(phase1),
                    r_alive * np.exp(phase2),
                )
            else:
                update_editor_values(
                    editable_grid,
                    qubits,
                    cell_selected,
                    alive_slider,
                    phase1_slider,
                    phase2_slider,
                )

        match game_mode:
            case GameMode.FUNCTIONAL:
                grid = functional_lattice.grid
            case GameMode.ENTANGLEMENT:
                grid = entangled_lattice.rendering_information
            case GameMode.HAMILTONIAN:
                grid = hamiltonian_lattice.grid

        grid_drawn = draw_grid(
            screen,
            game_mode,
            grid,
            pan,
            CELL_SIZE * scale,
            CELL_SIZE * SPACING * scale,
            h_dropdown.getSelected(),
            s_dropdown.getSelected(),
            v_dropdown.getSelected(),
        )

        for component in [
            alive_slider,
            phase1_slider,
            phase2_slider,
            alive_left_caption,
            alive_right_caption,
            alive_label,
            phase1_left_caption,
            phase1_right_caption,
            phase1_label,
            phase2_left_caption,
            phase2_right_caption,
            phase2_label,
        ]:
            if qubits:
                component.show()
            else:
                component.hide()

        for component in [
            function_dropdown,
            v_dropdown,
            s_dropdown,
            h_dropdown,
        ]:
            if game_mode == GameMode.FUNCTIONAL:
                component.show()
            else:
                component.hide()

        for component in [phase_toggle]:
            if game_mode == GameMode.HAMILTONIAN:
                component.show()
            else:
                component.hide()

        for component in [preset_button, preset_dropdown]:
            if game_mode == GameMode.ENTANGLEMENT:
                component.show()
            else:
                component.hide()

        mode_dropdown.show()

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

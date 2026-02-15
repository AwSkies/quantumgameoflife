import numpy as np
from enum import StrEnum
from .qubit import *

DELTA_THETA = 0.05


class Functions(StrEnum):
    ADDITION = "Addition"
    MULTIPLICATION = "Multiplication"
    PHASE_MOD_ADDITION = "θ, r Addition"
    GAUSSIAN_CONWAY = "Gaussian Conway"
    PHASE_FRIENDLY_GAUSSIAN_CONWAY = "Phase Friendly"
    CONWAY = "Conway"
    BOTCHED_CONWAY = "Botched Conway"


class Lattice:

    def __init__(self, x, y) -> None:
        self.grid = make_cell_array(x, y)
        random_initialize(self.grid)
        self.function = None

    def set_function(self, f):
        self.function = f

    def step(self):
        if self.function == None:
            self.function = Functions.CONWAY
        match self.function:
            case Functions.ADDITION:
                f = self.addition
            case Functions.MULTIPLICATION:
                f = self.multiplication
            case Functions.PHASE_MOD_ADDITION:
                f = self.phase_modulus_addition
            case Functions.GAUSSIAN_CONWAY:
                f = self.gaussian_conway
            case Functions.PHASE_FRIENDLY_GAUSSIAN_CONWAY:
                f = self.phase_friendly_gaussian_conway
            case Functions.CONWAY:
                f = self.conway
            case Functions.BOTCHED_CONWAY:
                f = self.botched_conway

        new_grid = self.grid.copy()

        for i, psi in np.ndenumerate(new_grid):
            f(psi, get_neighbors(self.grid, i))

        self.grid = new_grid
        normalize_cells(self.grid)

    def observe(self):
        for i, psi in np.ndenumerate(self.grid):
            if np.random.random() <= np.abs(np.square(psi["alive"])):
                set_cell_value(psi, 0, 1)
            else:
                set_cell_value(psi, 1, 0)

    def addition(self, cell, neighbors: list):
        a_new = np.sum([n["dead"] for n in neighbors])
        b_new = np.sum([n["alive"] for n in neighbors])
        set_cell_value(cell, a_new, b_new)

    def multiplication(self, cell, neighbors: list):
        a_new = np.prod([n["dead"] for n in neighbors])
        b_new = np.prod([n["alive"] for n in neighbors])
        set_cell_value(cell, a_new, b_new)

    def phase_modulus_addition(self, cell, neighbors: list):
        N = len(neighbors)
        a_new = (
            np.sum([np.abs(n["dead"]) for n in neighbors])
            / N
            * np.exp(1j * np.sum([np.angle(n["dead"]) for n in neighbors]))
        )
        b_new = (
            np.sum([np.abs(n["alive"]) for n in neighbors])
            / N
            * np.exp(1j * np.sum([np.angle(n["alive"]) for n in neighbors]))
        )
        set_cell_value(cell, a_new, b_new)

    def gaussian_conway(self, cell, neighbors: list):
        N = np.abs(np.sum([n["alive"] for n in neighbors]))
        b_mod = np.exp(-np.square(N - 2.5) / 0.5)
        a_mod = np.sqrt(1 - np.square(b_mod))
        a_phase = np.sum([np.angle(n["dead"]) for n in neighbors])
        b_phase = np.sum([np.angle(n["alive"]) for n in neighbors])
        set_cell_value(cell, a_mod * np.exp(1j * a_phase), b_mod * np.exp(1j * b_phase))

    def phase_friendly_gaussian_conway(self, cell, neighbors: list):
        N = np.abs(np.sum([n["alive"] for n in neighbors]))
        b_mod = np.exp(-np.square(N - 1.5) / 0.15)
        a_mod = np.sqrt(1 - np.square(b_mod))
        a_phase = np.sum([np.angle(n["dead"]) for n in neighbors])
        b_phase = np.sum([np.angle(n["alive"]) for n in neighbors])
        set_cell_value(cell, a_mod * np.exp(1j * a_phase), b_mod * np.exp(1j * b_phase))

    def conway(self, cell, neighbors: list):
        sum = np.sum([np.square(np.abs(n["alive"])) for n in neighbors])

        if sum < 2 or sum > 3:
            b_new = 0
        elif np.abs(np.abs(cell["dead"]) - 1.0) < 0.1:
            if np.abs(sum - 3) < 0.1:
                b_new = 1
            else:
                b_new = 0
        else:
            b_new = 1

        a_new = np.sqrt(1 - np.square(b_new))
        set_cell_value(cell, a_new, b_new)

    def botched_conway(self, cell, neighbors: list):
        sum = np.sum([np.square(np.abs(n["alive"])) for n in neighbors])

        if sum < 2 or sum > 3:
            b_new = 0
        elif np.abs(np.abs(cell["alive"]) - 1.0) < 0.1:
            if np.abs(sum - 3) < 0.1:
                b_new = 1
            else:
                b_new = 0
        else:
            b_new = 1

        a_new = np.sqrt(1 - np.square(b_new))
        set_cell_value(cell, a_new, b_new)

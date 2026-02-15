import numpy as np
from enum import StrEnum
from .qubit import *

class Functions(StrEnum):
    ADDITION = "Addition"
    MULTIPLICATION = "Multiplication"
    CONWAY = "Conway"
    BOTCHED_CONWAY = "Botched conway"

class Lattice:

    def __init__(self, x, y) -> None:
        self.grid = make_cell_array(x, y)
        fixed_initialize(self.grid, 1, 0)
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
            case Functions.CONWAY:
                f = self.conway
            case Functions.BOTCHED_CONWAY:
                f = self.botched_conway

        new_grid = self.grid.copy()

        for i, psi in np.ndenumerate(new_grid):
            f(psi, get_neighbors(self.grid, i))

        self.grid = new_grid
        normalize_cells(self.grid)

    def addition(self, cell, neighbors: list):
        a_new = np.sum([n["dead"] for n in neighbors])
        b_new = np.sum([n["alive"] for n in neighbors])
        set_cell_value(cell, a_new, b_new)

    def multiplication(self, cell, neighbors: list):
        a_new = np.prod([n["dead"] for n in neighbors])
        b_new = np.prod([n["alive"] for n in neighbors])
        set_cell_value(cell, a_new, b_new)

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

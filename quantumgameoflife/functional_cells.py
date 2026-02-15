import numpy as np
from enum import StrEnum

seed_value = 10
FUNCTIONAL_CELL_TYPE = np.dtype([("dead", np.complex128), ("alive", np.complex128)])


def make_cell_array(x, y):
    return np.zeros((x, y), dtype=FUNCTIONAL_CELL_TYPE)


def fixed_initialize(cell_matrix, a, b):
    for i, c in np.ndenumerate(cell_matrix):
        c["dead"] = a
        c["alive"] = b
        normalize(c)


def random_initialize(cell_matrix):
    """
    Fill np matrix with random pairs of alive and dead complex number
    Args:
        np[][]
    """
    for row in cell_matrix:
        for cell in row:
            cell["dead"] = complex(
                np.random.default_rng().random(), np.random.default_rng().random()
            )
            cell["alive"] = complex(
                np.random.default_rng().random(), np.random.default_rng().random()
            )
            normalize(cell)


def normalize_cells(grid):
    for i, c in np.ndenumerate(grid):
        normalize(c)


def normalize(cell):
    norm = np.hypot(abs(cell["alive"]), abs(cell["dead"]))
    cell["dead"] /= norm
    cell["alive"] /= norm


def phase_difference(cell):
    """
    phase angle: alive - dead
    return: float64 (-pi, pi]
    """
    return np.angle(cell["alive"] / cell["dead"])


def set_cell_value(cell, c_dead, c_alive):
    cell["alive"] = c_alive
    cell["dead"] = c_dead


def get_neighbors(grid: np.ndarray, i: tuple[int, int]):
    neighbors = []
    for ri in [-1, 0, 1]:
        for ci in [-1, 0, 1]:
            x = i[0] + ri
            y = i[1] + ci
            s = np.shape(grid)
            if not (
                (ri == 0 and ci == 0) or (x < 0 or x >= s[0]) or (y < 0 or y >= s[1])
            ):
                neighbors.append(grid[i[0] + ri, i[1] + ci])
    return neighbors

class Functions(StrEnum):
    ADDITION = "Addition"
    MULTIPLICATION = "Multiplication"
    CONWAY = "Conway"

class Lattice:

    def __init__(self, x, y) -> None:
        self.grid = make_cell_array(x, y)
        fixed_initialize(self.grid, 0, 1 + 1j)
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

        for i, psi in np.ndenumerate(self.grid):
            f(psi, get_neighbors(self.grid, i))

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
        elif np.abs(cell["alive"]) < 0.5:
            if np.abs(sum - 3) < 0.1:
                b_new = 1
            else:
                b_new = 0
        else:
            b_new = 1

        a_new = np.sqrt(1 - np.square(b_new))
        set_cell_value(cell, a_new, b_new)


if __name__ == "__main__":
    matrix = make_cell_array(2, 2)
    random_initialize(matrix)
    print(matrix)

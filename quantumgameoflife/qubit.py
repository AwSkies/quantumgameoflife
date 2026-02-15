import numpy as np

QUBIT = np.dtype([("dead", np.complex128), ("alive", np.complex128)])


def make_cell_array(x, y):
    return np.zeros((x, y), dtype=QUBIT)


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
    return cell_matrix


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

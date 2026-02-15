import numpy as np
import copy
D_T= 0.05
from quantumgameoflife import functional_cells
LIFE_THRESHOLD = 0.5

def refresh_ghost_edges(grid):
    # assuming grid has ghost edges
    rows, cols = grid.shape

    # Top/bottom
    grid[0, 1:-1] = grid[-2, 1:-1]   # top row = last interior row
    grid[-1, 1:-1] = grid[1, 1:-1]   # bottom row = first interior row

    # Left/right
    grid[1:-1, 0] = grid[1:-1, -2]   # left column = last interior column
    grid[1:-1, -1] = grid[1:-1, 1]   # right column = first interior column

    # Corners
    grid[0, 0] = grid[-2, -2]        # top-left
    grid[0, -1] = grid[-2, 1]        # top-right
    grid[-1, 0] = grid[1, -2]        # bottom-left
    grid[-1, -1] = grid[1, 1]        # bottom-right

def add_ghost_edge(grid):
    rows, cols = grid.shape
    new_grid = np.zeros((rows + 2, cols + 2), dtype=grid.dtype)
    # Copy original grid into center
    new_grid[1:-1, 1:-1] = grid
    new_grid[0, 1:-1] = grid[-1, :] 
    new_grid[-1, 1:-1] = grid[0, :] #new grid bottom is old grid top
    new_grid[1:-1, 0] = grid[:, -1] #new grid left is old grid right
    new_grid[1:-1, -1] = grid[:, 0] #etc. 
    # Corner
    new_grid[0, 0] = grid[-1, -1]
    new_grid[0, -1] = grid[-1, 0]
    new_grid[-1, 0] = grid[0, -1]
    new_grid[-1, -1] = grid[0, 0]
    return new_grid

def hamiltonian_boolean_matrix(grid):
    boolean_grid = np.zeros(grid.shape, dtype=bool)
    row, coln = grid.shape
    for i in range(1, row - 1):
        for j in range(1, coln - 1):
            counter = 0.0
            for m in range(i-1, i+2):
                for n in range(j-1, j+2):
                    if(m == i and n == j):
                        continue
                    value = (np.abs(grid[m][n]['alive']) ** 2)* (1 - ((np.abs(np.angle(grid[i][j]['alive'] / grid[m][n]['alive'])) % np.pi) / np.pi))
                    if(value >= LIFE_THRESHOLD):
                        counter = counter + 1
            if(counter >= 2 and counter <= 3):
                boolean_grid[i][j] = True
            else:
                boolean_grid[i][j] = False
            counter = 0.0
    return boolean_grid

def update_grid(grid, boolean_grid):
    rows, cols = grid.shape

    # Only update interior cells
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if boolean_grid[i, j]:
                new_a = grid[i][j]['dead'] * np.cos(D_T) - 1j * grid[i][j]['alive'] * np.sin(D_T)
                new_b = grid[i][j]['alive'] * np.cos(D_T) - 1j * grid[i][j]['dead'] * np.sin(D_T)
                functional_cells.set_cell_value(grid[i][j], new_a, new_b)

    # no need to handle edges manually
    return grid


def propogation_non_entangled(grid):
    #new_grid = add_ghost_edge(old_grid)
    boolean = hamiltonian_boolean_matrix(grid)
    #boolean = np.zeros(grid.shape)
    update_grid(grid, boolean)
    refresh_ghost_edges(grid) 
    return grid
import numpy as np
D_T= 0.01
from quantumgameoflife import cells

def add_ghost_edge(grid):
    rows, cols = grid.shape
    new_grid = np.zeros((rows + 2, cols + 2), dtype=grid.dtype)
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
    boolean_grid = np.zeros(grid.shape)
    return boolean_grid

def update_grid(grid):
    rows, cols = grid.shape
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            new_a = grid[i][j]['dead'] * np.cos(D_T) - 1j * grid[i][j]['alive'] * np.sin(D_T)
            new_b = grid[i][j]['alive'] * np.cos(D_T) - 1j * grid[i][j]['dead'] * np.sin(D_T)
            cells.set_cell_value(grid, new_a, new_b)
    #handle edges: 
    grid[0, 1:-1] = grid[-2, 1:-1] 
    grid[-1, 1:-1] = grid[1, 1:-1 ] #new grid bottom is old grid top
    grid[1:-1, 0] = grid[1:-1, -2] #new grid left is old grid right
    grid[1:-1, -1] = grid[1:-1, 1] #etc. 
    #handle corners
    grid[0, 0] = grid[-2, -2]
    grid[0, -1] = grid[-2, 1]
    grid[-1, 0] = grid[1, -2]
    grid[-1, -1] = grid[1, 1]


def propogation_non_entangled(grid):
    #new_grid = add_ghost_edge(old_grid)
    update_grid(grid)
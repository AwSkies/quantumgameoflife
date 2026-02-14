import numpy as np

CELL_TYPE = np.dtype([('alive', np.complex128), ('dead', np.complex128)])


def make_cell_array(x, y):
    return np.zeros((x,y), dtype=CELL_TYPE)

def random_initialize(cell_matrix):
    '''
    Fill np matrix with random pairs of alive and dead complex number
    
    Args: 
        np[][]
    '''
    for row in cell_matrix: 
        for cell in row: 
            cell['alive'] = complex(np.random.default_rng().random(), np.random.default_rng().random())
            cell['dead'] = complex(np.random.default_rng().random(), np.random.default_rng().random())
            normalization(cell)

def renormalize_cell_array(cell_matrix):
    for row in cell_matrix: 
        for cell in row: 
            normalization(cell)

def normalization(cell):
    norm = np.sqrt(abs(cell['alive']) ** 2 + abs(cell['dead']) ** 2)
    cell['alive'] /= norm
    cell['dead'] /= norm

def phase_difference(cell):
    '''
    phase angle: alive - dead
    return: float64 (-pi, pi]
    '''
    return np.angle(cell['alive'] / cell['dead'])

def set_cell_value(cell, c_alive, c_dead):
    cell['alive'] = c_alive
    cell['dead'] = c_dead

if __name__ == '__main__':
    matrix = make_cell_array(2, 2)
    random_initialize(matrix)
    print(matrix)
    


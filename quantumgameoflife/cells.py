import numpy as np

CELL_TYPE = np.dtype([('alive', np.complex128), ('dead', np.complex128)])


def make_cell_array(x, y):
    return np.zeros((x,y), dtype=CELL_TYPE)


if __name__ == '__main__':
    print(make_cell_array(2, 2))


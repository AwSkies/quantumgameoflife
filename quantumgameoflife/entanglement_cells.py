import numpy as np


class Lattice:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        #an array of states; self.states[n] = a 3 x 3 array representing the nth state
        self.states = create_states()


        self.next_center_states = np.array([next_center_state(self.states[i]) for i in range(0, 512)])

        #grid in ford [x, y, an], with a coefficient of nth state
        self.grid = create_cells

        #self.states_alive[neighbour_number, state_group_number] = [list of state indices in neighbour]
        #self.states_dead[neighbour_number, state_group_number]

        # self.state_group[neighbour_number, state_number]

        #self.common_indices_1[neighbour_number] gives indices in common for a cell with its neighbour
        #neigbour number 0 is cell directly up, then it goes clockwise



        self.common_indices_1 = [
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
            [(0, 1), (0, 2), (1, 1), (1, 2)],
            [(0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (2, 2)],
            [(1, 1), (1, 2), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (2, 0), (2, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)]
        ]

        # print(self.states[1][self.common_indices_1[0]])
        # r, c = zip(*[(1, 1),(0, 0), (0, 0)])
        # print(self.states[1][r, c])

        self.common_indices_neighbour = [self.common_indices_1[(i + 4) % 8] for i in range(8)]

        self.state_group_number = np.zeros((512, 8), dtype=int)

        self.states_alive = []
        self.states_dead = []

        for neighbour_number in range(8):
            self.states_alive.append([])
            self.states_dead.append([])
            common_indices_1 = self.common_indices_1[neighbour_number]
            common_indices_neighbour = self.common_indices_neighbour[neighbour_number]

            r_1, c_1 = zip(*common_indices_1)
            r_neighbour, c_neighbour = zip(*common_indices_neighbour)

            # state_1 = np.zeros((3, 3), dtype=bool)
            # state_neighbour = np.zeros((3, 3), dtype=bool)

            n_common_indices = len(common_indices_1)
            for state_group_number in range(n_common_indices):
                self.states_alive[-1].append([])
                self.states_dead[-1].append([])
                b_array = nth_binary_array(state_group_number, n_common_indices)
                # state_1[common_indices_1] = b_array
                # state_neighbour[common_indices_neighbour] = b_array

                for i in range(512):
                    state = self.states[i]
                    if np.all(state[r_1, c_1] == b_array):
                        self.state_group_number[i] = state_group_number
                        for j in range(512):
                            state_j = self.states[j]
                            if np.all(state_j[r_neighbour, c_neighbour] == b_array):
                                if self.next_center_states[j]:
                                    self.states_alive[-1][-1].append(j)
                                else:
                                    self.states_dead[-1][-1].append(j)


    def get_coefficients_for_index_values(self, pos, offset, state, coefficient_grid):
        

        #
    # def update_grid(self):
    #     get_shifted_probabilities()


def create_cells(x: int, y: int):
    return np.zeros((x, y, 512), dtype=np.complex128)

def create_states():
    n = 9
    total = 2 ** n
    numbers = np.arange(total)
    binary_arrays = ((numbers[:, None] >> np.arange(n - 1, -1, -1)) & 1)
    states = binary_arrays.reshape(512, 3, 3)
    states = states[:, ::-1, ::-1]
    return states.astype(bool)

def get_state_number(state):
    s = 0
    for i in range(9):
        s += 2**i * state[i // 3, i % 3]
    return s

def next_center_state(grid):
    """
    grid: 3x3 numpy array of dtype bool
    Returns: bool (next state of center cell)
    """
    assert grid.shape == (3, 3)

    center = grid[1, 1]

    # Count alive neighbors (exclude center cell)
    live_neighbors = np.sum(grid) - center

    if center:
        # Alive cell survives with 2 or 3 neighbors
        return live_neighbors in (2, 3)
    else:
        # Dead cell becomes alive with exactly 3 neighbors
        return live_neighbors == 3



def nth_binary_array(n, k):
    """
    Returns the nth binary array of length k.
    n: integer (0 <= n < 2^k)
    k: length of binary array
    """
    if n < 0 or n >= 2**k:
        raise ValueError("n must satisfy 0 <= n < 2^k")

    return ((n >> np.arange(k-1, -1, -1)) & 1).astype(int)

print(nth_binary_array(4, 6))

l = Lattice(10, 10)
# states = create_states()
# print(states)



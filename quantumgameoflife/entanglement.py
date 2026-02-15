import random
from quantumgameoflife.shapes import *

import numpy as np
import pickle
RENDER_PHASE = True
CONFIGURATION_NUMBER = 5

class Lattice:
    def __init__(self, x : int, y : int, configuration_number=CONFIGURATION_NUMBER, render_phase=RENDER_PHASE):
        self.x = x
        self.y = y
        self.dims = np.array([x, y])
        self.cutoff_for_states = 0.8

        #an array of states; self.states[n] = a 3 x 3 array representing the nth state
        self.states = create_states()

        self.next_center_states = np.array([next_center_state(self.states[i]) for i in range(0, 512)])

        self.steps_done = 0

        #grid in ford [x, y, an], with a coefficient of nth state
        self.initialize_grid(x, y, configuration_number)
        self.alive_magnitudes = np.zeros((x, y))
        self.magnitudes = np.zeros((x, y))
        self.rendering_information = np.zeros((x, y), np.dtype([("mag", float), ("sat", float), ("angle", float)]))
        if render_phase:
            self.rendering_information["sat"] = 100

        self.normalize_grid_and_update_magnitudes()
        # print(self.grid[:, :, 0])
        # print(self.alive_magnitudes)

        #self.states_alive[neighbour_number, state_group_number] = [list of state indices in neighbour]
        #self.states_dead[neighbour_number, state_group_number]

        # self.state_group[neighbour_number, state_number]

        #self.common_indices_1[neighbour_number] gives indices in common for a cell with its neighbour
        #neigbour number 0 is cell directly up, then it goes clockwise

        self.neighbour_offsets = np.array([
            [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]
        ])

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

        self.common_indices_neighbour = [self.common_indices_1[(i + 4) % 8] for i in range(8)]


        #change orders of indices:
        new_neighbour_ordering = [7, 0, 1, 6, 2, 5, 4, 3]
        self.neighbour_offsets = self.neighbour_offsets[new_neighbour_ordering]
        self.common_indices_neighbour = [self.common_indices_neighbour[i] for i in new_neighbour_ordering]
        self.common_indices_1 = [self.common_indices_1[i] for i in new_neighbour_ordering]

        try:
            with open('stored_state_information.pkl', 'rb') as f:
                stored_values = pickle.load(f)
            self.state_group_number = stored_values['state_group_number']
            self.states_alive = stored_values['states_alive']
            self.states_dead = stored_values['states_dead']

        except:
            self.state_group_number = np.zeros((8, 512), dtype=int)

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
                for state_group_number in range(2**n_common_indices):
                    self.states_alive[-1].append([])
                    self.states_dead[-1].append([])
                    b_array = nth_binary_array(state_group_number, n_common_indices)
                    # state_1[common_indices_1] = b_array
                    # state_neighbour[common_indices_neighbour] = b_array

                    for i in range(512):
                        state = self.states[i]
                        if np.all(state[r_1, c_1] == b_array):
                            self.state_group_number[neighbour_number, i] = state_group_number
                    for j in range(512):
                        state_j = self.states[j]
                        if np.all(state_j[r_neighbour, c_neighbour] == b_array):
                            if self.next_center_states[j]:
                                self.states_alive[-1][-1].append(j)
                            else:
                                self.states_dead[-1][-1].append(j)

            state_information = {
                'state_group_number': self.state_group_number,
                'states_alive': self.states_alive,
                'states_dead': self.states_dead,
            }
            with open('stored_state_information.pkl', 'wb') as f:
                pickle.dump(state_information, f)

        # print(self.states[self.states_alive[3][self.state_group_number[3, 41]]][1])
        # print(self.states[41])
        #
        # print(self.states_alive[0][self.state_group_number[0, 0]])
        #

        # print(self.states[1])

        # self.test()
        # 1/0

    def set_to_preset(self, configuration_number):
        self.initialize_grid(self.x, self.y, configuration_number)
        self.normalize_grid_and_update_magnitudes()

    def test(self):
        current_coefficients = np.ones(512)
        state_numbers = np.array([4])
        # coefficient_sets = np.array([self.get_coefficients_for_state(pos, state_number) for state_number in state_numbers])
        # coefficient_sets = np.array([[[0, 1], [1, 0], [1, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]], [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0.5, 1]]])
        # coefficient_sets = np.array([[1, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0.5, 1]])
        coefficient_sets = np.array([[[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]]])
        # coefficient_sets = np.array([[[0, 1], [0, 1], [0, 1], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0]]])
        # Assuming coefficient_sets has shape (n, 8, 2)
        n = coefficient_sets.shape[0]

        # Start with the first row for all n samples
        r = coefficient_sets[:, -1, :].copy()  # shape (n, 2)

        # Iteratively compute products
        for i in range(6, -1, -1):
            # print(i)
            # r[:, :, np.newaxis] has shape (n, current_size, 1)
            # a[:, i, np.newaxis, :] has shape (n, 1, 2)
            # Broadcasting creates (n, current_size, 2), then flatten last two dims
            r = (r[:, :, np.newaxis] * coefficient_sets[:, i, np.newaxis, :]).reshape(n, -1)
            # r = np.concat(r[])

        # r = r[:, ::-1]
        alive_indices = self.next_center_states[state_numbers]
        states_alive = r[alive_indices] * current_coefficients[state_numbers[alive_indices]][:, np.newaxis]
        states_dead = r[~alive_indices] * current_coefficients[state_numbers[~alive_indices]][:, np.newaxis]

        new_coefficient_sets_alive = np.sum(states_alive, axis=0)
        new_coefficient_sets_dead = np.sum(states_dead, axis=0)

        new_coefficients = np.concatenate([new_coefficient_sets_dead, new_coefficient_sets_alive])

        st = np.where(new_coefficients)
        # print(st)
        # print(self.states[st[0]])

    def run(self):
        while 1:
            self.step()
            # print(self.alive_magnitudes)

    def step(self):
        self.update_cells()
        self.steps_done += 1

    def update_cells(self):
        pos = np.array([0, 0])
        all_state_numbers = np.arange(0, 512)

        if self.steps_done == 1:
            pass

        new_grid = np.zeros_like(self.grid)
        for x in range(self.x):
            # print(f"x: {x}")
            pos[1] = 0
            for y in range(self.y):
                if (x, y) == (2, 3):
                    pass
                # print(f"y: {y}")
                if self.cutoff_for_states:
                    state_numbers = self.get_more_prominent_states(self.magnitudes[pos[0], pos[1]], self.cutoff_for_states)
                else:
                    state_numbers = all_state_numbers
                new_coefficients = self.get_new_cell_coefficients(pos, state_numbers, self.grid[pos[0], pos[1]])
                new_grid[pos[0], pos[1]] = new_coefficients
                pos[1] += 1
            pos[0] += 1
        self.grid = new_grid
        self.normalize_grid_and_update_magnitudes()

    def remove_0_states(self):
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if not np.any(self.grid[x, y]):
                    self.grid[x, y, 0] = 1

    def initialize_grid(self, x, y, configuration_number):

        # configuration_number = 8

        if configuration_number == 0: #blinker
            indices = [(2,1), (2, 2), (2, 3)]
            self.grid = self.get_grid_for_single_state(x, y, indices)
        elif configuration_number == 1:  # glider
            indices = np.array([(3,1), (3, 2), (3, 3), (2, 3), (1, 2)])
            self.grid = self.get_grid_for_single_state(x, y, indices)
        elif configuration_number == 2: #2 glider, superposition
            indices1 = np.array([(3,1), (3, 2), (3, 3), (2, 3), (1, 2)])
            indices2 = (indices1 + np.array([4, 4])) % np.array([x, y])
            grid1 = self.get_grid_for_single_state(x, y, indices1)
            grid2 = self.get_grid_for_single_state(x, y, indices2)
            self.grid = grid1 + grid2
        elif configuration_number in [3, 4, 5]: #2 gliders, interfering superposition
            indices1 = np.array([(3,1), (3, 2), (3, 3), (2, 3), (1, 2)])
            indices2 = np.array([(3,1), (3, 2), (3, 3), (4, 1), (5, 2)])
            indices2 = (indices2 + np.array([6, 4])) % np.array([x, y])
            grid1 = self.get_grid_for_single_state(x, y, indices1)
            if configuration_number == 3:
                phase = np.pi*0.2
            elif configuration_number == 4:
                phase = np.pi*0.5
            else:
                phase = 0
            grid2 = np.exp(phase * 1j)*self.get_grid_for_single_state(x, y, indices2)
            self.grid = grid2 + grid1

        elif configuration_number == 6: #superposition of random gliders
            indices1 = np.array([(3, 1), (3, 2), (3, 3), (2, 3), (1, 2)])
            indices2 = np.array([(3, 1), (3, 2), (3, 3), (4, 1), (5, 2)])
            indices3 = np.array([(3, 1), (3, 2), (3, 3), (2, 1), (1, 2)])
            indices4 = np.array([(3, 1), (3, 2), (3, 3), (4, 3), (5, 2)])

            indices_sets = [indices1, indices2, indices3, indices4]

            grid = np.zeros((x, y, 512), dtype=np.complex128)

            for i in range(7):
                indices = random.choice(indices_sets)
                indices = (indices + np.array([random.randint(0, x), random.randint(0, y)])) % np.array([x, y])
                phase = random.uniform(0, 2 * np.pi)
                # phase = np.pi/2
                grid += self.get_grid_for_single_state(x, y, indices) * np.exp(1j * phase)

            self.grid = grid

        elif configuration_number == 7: #superposition of random gliders
            grid = np.zeros((x, y, 512), dtype=np.complex128)
            grid += 2**(1 + np.random.rand(x, y, 512)*5)
            # grid = np.random.rand(x, y, 512) + np.random.rand(x, y, 512)*1j
            self.grid = grid

        elif configuration_number == 8: #block and glider
            grid = np.zeros((x, y, 512), dtype=np.complex128)
            indices1 = np.array([(3, 1), (3, 2), (3, 3), (2, 3), (1, 2)])
            block_indices = np.array([[6, 6], [6, 7], [7, 6], [7, 7]]) + 5
            grid += 1j* self.get_grid_for_single_state(x, y, indices1)
            grid +=  self.get_grid_for_single_state(x, y, block_indices)
            self.grid = grid

        elif configuration_number == 9: #pulsar
            pulsar = PULSAR
            pulsar_x, pulsar_y = pulsar.shape

            corner = (2, 2)
            binary_array = np.zeros((x, y), dtype=int)
            # binary_array[corner[0]:corner[0]+pulsar_x, corner[1]+pulsar_y] = 1
            binary_array[corner[0]:corner[0]+pulsar_x, corner[1]:corner[1]+pulsar_y] = pulsar
            grid = self.get_grid_for_single_state(x, y, binary_array=binary_array)
            self.grid = grid

        elif configuration_number == 10: #pulsar block superposition

            pulsar_x, pulsar_y = PULSAR.shape

            corner = (2, 2)
            binary_array = np.zeros((x, y), dtype=int)
            # binary_array[corner[0]:corner[0]+pulsar_x, corner[1]+pulsar_y] = 1
            binary_array[corner[0]:corner[0] + pulsar_x, corner[1]:corner[1] + pulsar_y] = PULSAR
            grid = self.get_grid_for_single_state(x, y, binary_array=binary_array)

            # block_indices = np.array([[6, 6], [6, 7], [7, 6], [7, 7]]) + 5
            # grid_block = self.get_grid_for_single_state(x, y, block_indices)
            #
            # self.grid = grid + (0.3 + 0.1j)* grid_block

            grid_2 = np.roll(grid, (4, 4))
            self.grid = grid + 1j*grid_2

        elif configuration_number == 11:
            hw_x, hw_y = HWSS.shape
            corner = (2, 2)
            binary_array = np.zeros((x, y), dtype=int)
            binary_array[corner[0]:corner[0] + hw_x, corner[1]:corner[1] + hw_y] = HWSS
            grid = self.get_grid_for_single_state(x, y, binary_array=binary_array)

            binary_array_2 = np.roll(binary_array[::-1, :], (-5, 5))
            grid2 = self.get_grid_for_single_state(x, y, binary_array=binary_array_2)

            self.grid = grid + np.exp((np.pi/2) *1j) * grid2

        elif configuration_number == 12:
            hw_x, hw_y = HWSS.shape
            corner = (2, 2)
            # print(x, y)
            binary_array = np.zeros((x, y), dtype=int)
            binary_array[corner[0]:corner[0] + hw_x, corner[1]:corner[1] + hw_y] = HWSS
            grid = self.get_grid_for_single_state(x, y, binary_array=binary_array)

            binary_array_2 = np.roll(binary_array[::-1, :], (-5, 5))
            grid2 = self.get_grid_for_single_state(x, y, binary_array=binary_array_2)

            self.grid = grid + np.exp(0.7j) * grid2

        elif configuration_number == 13:
            grid = np.zeros((x, y, 512), dtype=np.complex128)
            grid += np.random.rand(x, y, 512)*1j
            grid += np.random.rand(x, y, 512)
            self.grid = grid

        else:
            raise(NotImplementedError)



    def get_grid_for_single_state(self, x, y, indices=None, binary_array=None):

        if np.any(indices):
            binary_grid = np.zeros((x, y))
            for index in indices:
                binary_grid[index[0], index[1]] = 1
        else:
            binary_grid = binary_array

        grid = np.zeros((x, y, 512), dtype=np.complex128)
        for i in range(x):
            for j in range(y):
                rows = [(i - 1) % x, i % x, (i + 1) % x]
                cols = [(j - 1) % y, j % y, (j + 1) % y]

                subarray = binary_grid[np.ix_(rows, cols)]
                state_number = get_state_number(subarray)
                grid[i, j, state_number] = 1

        return grid

    def add_pos(self, pos, offset):
        return (pos + offset) % self.dims

    def get_coefficients_for_index_values(self, pos, neighbour_number, state_number, coefficient_grid):
        neighbour_states_alive = self.states_alive[neighbour_number][self.state_group_number[neighbour_number, state_number]]
        neighbour_states_dead = self.states_dead[neighbour_number][self.state_group_number[neighbour_number, state_number]]
        neighbour_pos = self.add_pos(pos, self.neighbour_offsets[neighbour_number])
        alive_coefficients = coefficient_grid[neighbour_pos[0], neighbour_pos[1], neighbour_states_alive]
        dead_coefficients = coefficient_grid[neighbour_pos[0], neighbour_pos[1], neighbour_states_dead]
        # return np.sum(np.abs(dead_coefficients)**2)**0.5, np.sum(np.abs(alive_coefficients)**2)**0.5
        return np.sum(dead_coefficients), np.sum(alive_coefficients)

    def get_coefficients_for_state(self, pos, state_number):
        coefficients = np.zeros((8, 2), dtype=np.complex128)
        for neighbour_number in range(8):
            coefficients[neighbour_number] = self.get_coefficients_for_index_values(pos, neighbour_number, state_number, self.grid)
        return coefficients

    def normalize_grid_and_update_magnitudes(self):
        self.remove_0_states()
        magnitudes = np.abs(self.grid)**2
        cell_magnitudes = np.sum(magnitudes, axis=2)
        # print(cell_magnitudes)

        # print(cell_magnitudes.shape)
        self.grid = self.grid / cell_magnitudes[:, :, np.newaxis]**0.5
        self.magnitudes = np.abs(self.grid) ** 2
        self.alive_magnitudes = np.sum(self.magnitudes[:, :, 256::], axis=2)
        self.alive_magnitudes = np.nan_to_num(self.alive_magnitudes, nan=0.0)
        # print(self.alive_magnitudes)
        # print(np.sum(self.grid[:, :, 256::]))
        self.alive_angles = np.angle(np.sum(self.grid[:, :, 256::], axis=2))
        self.alive_angles = (self.alive_angles * 180 / np.pi) % 360
        self.rendering_information["mag"] = self.alive_magnitudes
        self.rendering_information["angle"] = self.alive_angles

        # print(self.alive_angles)

    def get_state_numbers(self):
        return np.arange(0, 512)

    def get_more_prominent_states(self, magnitudes, cutoff):
        indices = np.argsort(magnitudes)[::-1]
        sorted_magnitudes = magnitudes[indices]
        s = 0
        for i in range(len(indices)):
            s += sorted_magnitudes[i]
            if s >= cutoff:
                return indices[:i+1]
        return indices

    def get_new_cell_coefficients(self, pos, state_numbers, current_coefficients):
        coefficient_sets = np.array([self.get_coefficients_for_state(pos, state_number) for state_number in state_numbers])
        # coefficient_sets = np.array([[[0, 1], [1, 0], [1, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]], [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0.5, 1]]])
        # coefficient_sets = np.array([[1, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0.5, 1]])

        # Assuming coefficient_sets has shape (n, 8, 2)
        n = coefficient_sets.shape[0]

        r = coefficient_sets[:, -1, :].copy()  # shape (n, 2)

        # Iteratively compute products
        for i in range(6, -1, -1):
            r = (r[:, :, np.newaxis] * coefficient_sets[:, i, np.newaxis, :]).reshape(n, -1)
            # r = np.concat(r[])

        alive_indices = self.next_center_states[state_numbers]
        states_alive = r[alive_indices]*current_coefficients[state_numbers[alive_indices]][:, np.newaxis]
        states_dead = r[~alive_indices]*current_coefficients[state_numbers[~alive_indices]][:, np.newaxis]

        new_coefficient_sets_alive = np.sum(states_alive, axis=0)
        new_coefficient_sets_dead = np.sum(states_dead, axis=0)

        new_coefficients = np.concatenate([new_coefficient_sets_dead, new_coefficient_sets_alive])
        if not np.any(new_coefficients):
            new_coefficients[0] = 1
        return new_coefficients

def create_states():
    n = 9
    total = 2 ** n
    numbers = np.arange(total)
    binary_arrays = ((numbers[:, None] >> np.arange(n - 1, -1, -1)) & 1)
    # binary_arrays = binary_arrays[:, [0, 1, 2, 3, 5, 6, 7, 8, 4]]
    indices = np.array([[0, 1, 2],
                        [3, 8, 4],
                        [5, 6, 7]])
    indices = -indices + 8
    states = binary_arrays[:, indices]
    # states = binary_arrays.reshape(512, 3, 3)
    # states = states[:, ::-1, ::-1]
    return states.astype(bool)

def get_state_number(state):
    s = 0
    indices = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2], [1, 1]])
    for i in range(9):
        s += 2**i * state[indices[i, 0], indices[i, 1]]
    return int(s)

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
        # return live_neighbors in (1, 2, 3, 4, 5, 6)
    else:
        # Dead cell becomes alive with exactly 3 neighbors
        # return live_neighbors in (0, 3)
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


if __name__=="__main__":
    l = Lattice(5, 5)
    l.run()

# l.update_cell_coefficients(np.array([1, 1]), [1])
# states = create_states()
# print(states)



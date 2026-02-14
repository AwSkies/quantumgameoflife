import cv2
import cmath
import random
import colorsys
import matplotlib.pyplot as plt
#random.seed(10)
class cell: 
    def __init__(self):
        self.a = 0 + 0j
        self.b = 0 + 0j
        self.phase = 0

    def normalize(self):
        norm = cmath.sqrt(abs(self.a)**2 + abs(self.b)**2)
        self.a = self.a / norm
        self.b = self.b / norm
    
    def random_initialize(self):
        self.a = complex(random.random(), random.random())
        self.b = complex(random.random(), random.random())
        self.normalize()
    def phase_difference(self):
        self.phase = self.a.imag - self.b.imag

def create_cell_matrix(width, height):
    #return [[cell() for _ in range(width)] for _ in range(height)]
    return [[cell() for _ in range(height)] for _ in range(width)]
test_cell = cell()
test_cell.random_initialize()
print("Hello")
print(test_cell.a, test_cell.b)

def visualize_color_space(width=5, height=5):
    grid = []
    cells = create_cell_matrix(width, height)
    counter = 0
    step = 1.0 / (width * height)
    for y in range(height):
        row = []
        for x in range(width):
            #test_cell.random_initialize()
            cells[x][y].random_initialize()
            #cells[x][y].a.real
            #h = (cells[x][y].phase + cmath.pi )/ (2 * cmath.pi)
            h = 0.7
            s = counter#cells[x][y].b.real
            v = counter#cells[x][y].a.real
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            row.append([r, g, b])
            counter = counter + step
        grid.append(row)
    plt.imshow(grid)
    plt.axis("off")
    plt.show()
visualize_color_space()


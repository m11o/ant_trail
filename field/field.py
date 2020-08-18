import random
import numpy as np

class Field:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.field = np.zeros((X, Y), dtype=float)

    def shuffle_position(self):
        return [random.randrange(0, self.X), random.randrange(0, self.Y)]

    def is_left_end_line(self, y):
        return y == 0

    def is_right_end_line(self, y):
        return y == (self.Y - 1)

    def is_top_end_line(self, x):
        return x == 0

    def is_bottom_end_line(self, x):
        return x == (self.X - 1)

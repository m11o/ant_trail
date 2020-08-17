import random
import numpy as np

class Field:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.field = np.zeros((X, Y), dtype=float)

    def shuffle_position(self):
        return [random.randrange(0, self.X), random.randrange(0, self.Y)]
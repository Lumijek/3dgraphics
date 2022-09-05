import numpy as np


class CubeScreenTransformer:
    def __init__(self, width, height):
        self.x_factor = width / 2
        self.y_factor = height / 2

    def transform(self, v):
        inv_z = 1 / v[2]
        x = (v[0] * inv_z + 1) * self.x_factor
        y = (-v[1] * inv_z + 1) * self.y_factor
        return np.array([x, y, v[2]])

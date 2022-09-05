import numpy as np


class IndexedLineList:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices


class IndexedTriangleList:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices
        self.cull_flags = np.full(indices.shape[0], False)


class Cube:
    def __init__(self, size, origin):  # size is length of 1 side
        self.origin = origin
        self.calculate_vertices(size, origin)

    def calculate_vertices(self, size, origin):
        self.vertices = np.full((8, 3), origin, dtype=float)
        side = size / 2
        self.vertices[0] += [-side, -side, -side]
        self.vertices[1] += [side, -side, -side]
        self.vertices[2] += [-side, side, -side]
        self.vertices[3] += [side, side, -side]
        self.vertices[4] += [-side, -side, side]
        self.vertices[5] += [side, -side, side]
        self.vertices[6] += [-side, side, side]
        self.vertices[7] += [side, side, side]
        self.original_vertices = self.vertices

    def get_lines(self):
        lines = np.array(
            [
                [0, 1],
                [1, 3],
                [3, 2],
                [2, 0],
                [0, 4],
                [1, 5],
                [3, 7],
                [2, 6],
                [4, 5],
                [5, 7],
                [7, 6],
                [6, 4],
            ]
        )
        return IndexedLineList(self.vertices.copy(), lines)

    def get_triangles(self):
        triangles = np.array(
            [
                [0, 2, 1],
                [2, 3, 1],
                [1, 3, 5],
                [3, 7, 5],
                [2, 6, 3],
                [3, 6, 7],
                [4, 5, 7],
                [4, 7, 6],
                [0, 4, 2],
                [2, 4, 6],
                [0, 1, 4],
                [1, 5, 4],
            ]
        )

        return IndexedTriangleList(self.vertices.copy(), triangles)

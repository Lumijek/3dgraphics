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
        self.tc = np.zeros(8 * 2).reshape(8, 2)
        side = size / 2
        self.vertices[0] += [-side, -side, -side]
        self.tc[0] = [0, 1]
        self.vertices[1] += [side, -side, -side]
        self.tc[1] = [1, 1]
        self.vertices[2] += [-side, side, -side]
        self.tc[2] = [0, 0]
        self.vertices[3] += [side, side, -side]
        self.tc[3] = [1, 0]
        self.vertices[4] += [-side, -side, side]
        self.tc[4] = [1, 1]
        self.vertices[5] += [side, -side, side]
        self.tc[5] = [0, 1]
        self.vertices[6] += [-side, side, side]
        self.tc[6] = [1, 0]
        self.vertices[7] += [side, side, side]
        self.tc[7] = [0, 0]
        self.tverts = np.zeros(8 * 5).reshape(8, 5)
        for i in range(len(self.vertices)):
            self.tverts[i] = np.hstack((self.vertices[i], self.tc[i]))

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

    def get_textured_triangles(self):
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

        return IndexedTriangleList(self.tverts.copy(), triangles)

class CubeFolded:
    def __init__(self, size):  # size is length of 1 side
        self.calculate_vertices(size)

    def calculate_vertices(self, size):
        self.vertices = np.zeros(14 * 3).reshape(14, 3)
        self.tc = np.zeros(14 * 2).reshape(14, 2)
        side = size / 2
        self.vertices[0] = [-side, -side, -side]
        self.tc[0] = [1, 0]
        self.vertices[1] = [side, -side, -side]
        self.tc[1] = [0, 0]
        self.vertices[2] = [-side, side, -side]
        self.tc[2] = [1, 1]
        self.vertices[3] = [side, side, -side]
        self.tc[3] = [0, 1]
        self.vertices[4] = [-side, -side, side]
        self.tc[4] = [1, 1]
        self.vertices[5] = [side, -side, side]
        self.tc[5] = [0, 1]
        self.vertices[6] = [-side, side, side]
        self.tc[6] = [1, 0]
        self.vertices[7] = [side, side, side]
        self.tc[7] = [0, 0]
        self.vertices[8] = [-side, -side, -side]
        self.tc[8] = [1, 0]
        self.vertices[9] = [side, -side, -side]
        self.tc[9] = [0, 0]
        self.vertices[10] = [-side, -side, -side]
        self.tc[10] = [0, 1]
        self.vertices[11] = [-side, -side, side]
        self.tc[11] = [0, 0]
        self.vertices[12] = [side, -side, -side]
        self.tc[12] = [1, 1]
        self.vertices[13] = [side, -side, side]
        self.tc[13] = [1, 0]



        self.tverts = np.zeros(14 * 5).reshape(14, 5)
        for i in range(len(self.vertices)):
            self.tverts[i] = np.hstack((self.vertices[i], self.tc[i]))

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
                [4, 8, 5],
                [5, 8, 9],
                [2, 6, 3],
                [3, 6, 7],
                [4, 5, 7],
                [4, 7, 6],
                [2, 10, 11],
                [2, 11, 6],
                [12, 3, 7],
                [12, 7, 13],
            ]
        )
        return IndexedTriangleList(self.vertices.copy(), triangles)

    def get_textured_triangles(self):
        triangles = np.array(
            [
                [0, 2, 1],
                [2, 3, 1],
                [4, 8, 5],
                [5, 8, 9],
                [2, 6, 3],
                [3, 6, 7],
                [4, 5, 7],
                [4, 7, 6],
                [2, 10, 11],
                [2, 11, 6],
                [12, 3, 7],
                [12, 7, 13],
            ]
        )

        return IndexedTriangleList(self.tverts.copy(), triangles)

class CubeFoldedWrapped:
    def __init__(self, size):  # size is length of 1 side
        self.calculate_vertices(size)

    def calculate_vertices(self, size):
        self.vertices = np.zeros(14 * 3).reshape(14, 3)
        self.tc = np.zeros(14 * 2).reshape(14, 2)
        side = size / 2
        self.vertices[0] = [-side, -side, -side]
        self.tc[0] = [1, 0]
        self.vertices[1] = [side, -side, -side]
        self.tc[1] = [0, 0]
        self.vertices[2] = [-side, side, -side]
        self.tc[2] = [1, 1]
        self.vertices[3] = [side, side, -side]
        self.tc[3] = [0, 1]
        self.vertices[4] = [-side, -side, side]
        self.tc[4] = [1, 3]
        self.vertices[5] = [side, -side, side]
        self.tc[5] = [0, 3]
        self.vertices[6] = [-side, side, side]
        self.tc[6] = [1, 2]
        self.vertices[7] = [side, side, side]
        self.tc[7] = [0, 2]
        self.vertices[8] = [-side, -side, -side]
        self.tc[8] = [1, 4]
        self.vertices[9] = [side, -side, -side]
        self.tc[9] = [0, 4]
        self.vertices[10] = [-side, -side, -side]
        self.tc[10] = [2, 1]
        self.vertices[11] = [-side, -side, side]
        self.tc[11] = [2, 2]
        self.vertices[12] = [side, -side, -side]
        self.tc[12] = [-1, 1]
        self.vertices[13] = [side, -side, side]
        self.tc[13] = [-1, 2]



        self.tverts = np.zeros(14 * 5).reshape(14, 5)
        for i in range(len(self.vertices)):
            self.tverts[i] = np.hstack((self.vertices[i], self.tc[i]))

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
                [4, 8, 5],
                [5, 8, 9],
                [2, 6, 3],
                [3, 6, 7],
                [4, 5, 7],
                [4, 7, 6],
                [2, 10, 11],
                [2, 11, 6],
                [12, 3, 7],
                [12, 7, 13],
            ]
        )
        return IndexedTriangleList(self.vertices.copy(), triangles)

    def get_textured_triangles(self):
        triangles = np.array(
            [
                [0, 2, 1],
                [2, 3, 1],
                [4, 8, 5],
                [5, 8, 9],
                [2, 6, 3],
                [3, 6, 7],
                [4, 5, 7],
                [4, 7, 6],
                [2, 10, 11],
                [2, 11, 6],
                [12, 3, 7],
                [12, 7, 13],
            ]
        )

        return IndexedTriangleList(self.tverts.copy(), triangles)

class CubeSkinned:
    def __init__(self, size):  # size is length of 1 side
        self.calculate_vertices(size)

    def calculate_vertices(self, size):
        self.vertices = np.zeros(14 * 3).reshape(14, 3)
        self.tc = np.zeros(14 * 2).reshape(14, 2)
        side = size / 2
        self.vertices[0] = [-side, -side, -side]
        self.tc[0] = [1, 0]
        self.vertices[1] = [side, -side, -side]
        self.tc[1] = [0, 0]
        self.vertices[2] = [-side, side, -side]
        self.tc[2] = [1, 1]
        self.vertices[3] = [side, side, -side]
        self.tc[3] = [0, 1]
        self.vertices[4] = [-side, -side, side]
        self.tc[4] = [1, 3]
        self.vertices[5] = [side, -side, side]
        self.tc[5] = [0, 3]
        self.vertices[6] = [-side, side, side]
        self.tc[6] = [1, 2]
        self.vertices[7] = [side, side, side]
        self.tc[7] = [0, 2]
        self.vertices[8] = [-side, -side, -side]
        self.tc[8] = [1, 4]
        self.vertices[9] = [side, -side, -side]
        self.tc[9] = [0, 4]
        self.vertices[10] = [-side, -side, -side]
        self.tc[10] = [2, 1]
        self.vertices[11] = [-side, -side, side]
        self.tc[11] = [2, 2]
        self.vertices[12] = [side, -side, -side]
        self.tc[12] = [-1, 1]
        self.vertices[13] = [side, -side, side]
        self.tc[13] = [-1, 2]
        self.tc[:, 0] = (self.tc[:, 0] + 1) / 3
        self.tc[:, 1] = self.tc[:, 1] / 4



        self.tverts = np.zeros(14 * 5).reshape(14, 5)
        for i in range(len(self.vertices)):
            self.tverts[i] = np.hstack((self.vertices[i], self.tc[i]))

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
                [4, 8, 5],
                [5, 8, 9],
                [2, 6, 3],
                [3, 6, 7],
                [4, 5, 7],
                [4, 7, 6],
                [2, 10, 11],
                [2, 11, 6],
                [12, 3, 7],
                [12, 7, 13],
            ]
        )
        return IndexedTriangleList(self.vertices.copy(), triangles)

    def get_textured_triangles(self):
        triangles = np.array(
            [
                [0, 2, 1],
                [2, 3, 1],
                [4, 8, 5],
                [5, 8, 9],
                [2, 6, 3],
                [3, 6, 7],
                [4, 5, 7],
                [4, 7, 6],
                [2, 10, 11],
                [2, 11, 6],
                [12, 3, 7],
                [12, 7, 13],
            ]
        )

        return IndexedTriangleList(self.tverts.copy(), triangles)
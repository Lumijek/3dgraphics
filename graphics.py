import numpy as np
import pygame


class Graphics:
    def __init__(self, screen):
        self.screen = screen

    def draw_triangle(self, v0, v1, v2, c):
        if v1[1] < v0[1]:
            v0, v1 = v1, v0
        if v2[1] < v1[1]:
            v1, v2 = v2, v1
        if v1[1] < v0[1]:
            v0, v1 = v1, v0
        if v0[1] == v1[1]:
            if v1[0] < v0[0]:
                v0, v1 = v1, v0
            self.draw_flat_top_triangle(v0, v1, v2, c)
        elif v1[1] == v2[1]:
            if v2[0] < v1[0]:
                v1, v2 = v2, v1
            self.draw_flat_bottom_triangle(v0, v1, v2, c)
        else:
            alpha_split = (v1[1] - v0[1]) / (v2[1] - v0[1])
            vi = v0 + (v2 - v0) * alpha_split

            if v1[0] < vi[0]:
                self.draw_flat_bottom_triangle(v0, v1, vi, c)
                self.draw_flat_top_triangle(v1, vi, v2, c)

            else:
                self.draw_flat_bottom_triangle(v0, vi, v1, c)
                self.draw_flat_top_triangle(vi, v1, v2, c)

    def draw_flat_top_triangle(self, v0, v1, v2, c):
        m0 = (v2[0] - v0[0]) / (v2[1] - v0[1])
        m1 = (v2[0] - v1[0]) / (v2[1] - v1[1])

        y_start = int(np.ceil(v0[1] - 0.5))
        y_end = int(np.ceil(v2[1] - 0.5))
        px0 = m0 * (np.arange(y_start, y_end) + 0.5 - v0[1]) + v0[0]
        px1 = m1 * (np.arange(y_start, y_end) + 0.5 - v1[1]) + v1[0]

        x_start = np.ceil(px0 - 0.5).astype(int)
        x_end = np.ceil(px1 - 0.5).astype(int)

        surf = pygame.surfarray.pixels3d(self.screen)

        for i, y in enumerate(range(y_start, y_end)):
            surf[x_start[i] : x_end[i], y] = c
        del surf

    def draw_flat_bottom_triangle(self, v0, v1, v2, c):
        m0 = (v1[0] - v0[0]) / (v1[1] - v0[1])
        m1 = (v2[0] - v0[0]) / (v2[1] - v0[1])

        y_start = int(np.ceil(v0[1] - 0.5))
        y_end = int(np.ceil(v2[1] - 0.5))

        px0 = m0 * (np.arange(y_start, y_end) + 0.5 - v0[1]) + v0[0]
        px1 = m1 * (np.arange(y_start, y_end) + 0.5 - v0[1]) + v0[0]

        x_start = np.ceil(px0 - 0.5).astype(int)
        x_end = np.ceil(px1 - 0.5).astype(int)

        surf = pygame.surfarray.pixels3d(self.screen)
        for i, y in enumerate(range(y_start, y_end)):
            surf[x_start[i] : x_end[i], y] = c
        del surf

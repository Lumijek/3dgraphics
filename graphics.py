import numpy as np
import pygame
import sys
import math
from pprint import pprint

np.set_printoptions(suppress=True)

class Graphics:
    def __init__(self, screen):
        self.screen = screen

    def interpolate(self, src, dest, alpha):
        return src + (dest - src) * alpha

    def interpolate_to(self, src, dest, alpha):
        i1 = self.interpolate(src[:3], dest[:3], alpha)
        i2 = self.interpolate(src[3:], dest[3:], alpha)
        return np.hstack((i1, i2))

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

    def draw_textured_triangle(self, v0, v1, v2, texture):
        if v1[1] < v0[1]:
            v0, v1 = v1, v0
        if v2[1] < v1[1]:
            v1, v2 = v2, v1
        if v1[1] < v0[1]:
            v0, v1 = v1, v0
        if v0[1] == v1[1]:
            if v1[0] < v0[0]:
                v0, v1 = v1, v0
            self.draw_flat_top_textured_triangle(v0, v1, v2, texture)

        elif v1[1] == v2[1]:
            if v2[0] < v1[0]:
                v1, v2 = v2, v1
            self.draw_flat_bottom_textured_triangle(v0, v1, v2, texture)

        else:
            alpha_split = (v1[1] - v0[1]) / (v2[1] - v0[1])
            vi = self.interpolate_to(v0, v2, alpha_split)

            if v1[0] < vi[0]:
                self.draw_flat_bottom_textured_triangle(v0, v1, vi, texture)
                self.draw_flat_top_textured_triangle(v1, vi, v2, texture)

            else:
                self.draw_flat_bottom_textured_triangle(v0, vi, v1, texture)
                self.draw_flat_top_textured_triangle(vi, v1, v2, texture)

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

    def draw_flat_top_textured_triangle(self, v0, v1, v2, texture):
        m0 = (v2[0] - v0[0]) / (v2[1] - v0[1])
        m1 = (v2[0] - v1[0]) / (v2[1] - v1[1])

        y_start = int(np.ceil(v0[1] - 0.5))
        y_end = int(np.ceil(v2[1] - 0.5))

        tcEdgeL = v0[3:].copy()
        tcEdgeR = v1[3:].copy()
        tcBottom = v2[3:].copy()

        tcEdgeStepL = (tcBottom - tcEdgeL) / (v2[1] - v0[1])
        tcEdgeStepR = (tcBottom - tcEdgeR) / (v2[1] - v1[1])

        tcEdgeL += tcEdgeStepL * (y_start + 0.5 - v1[1])
        tcEdgeR += tcEdgeStepR * (y_start + 0.5 - v1[1])
        tcEdgeL = tcEdgeL + np.arange(0, y_end - y_start)[:, None] * tcEdgeStepL
        tcEdgeR = tcEdgeR + np.arange(0, y_end - y_start)[:, None] * tcEdgeStepR

        tex_width = texture.get_width()
        tex_height = texture.get_height()
        tex_clamp_x = tex_width - 1
        tex_clamp_y = tex_height - 1

        px0 = m0 * (np.arange(y_start, y_end) + 0.5 - v0[1]) + v0[0]
        px1 = m1 * (np.arange(y_start, y_end) + 0.5 - v1[1]) + v1[0]

        x_start = np.ceil(px0 - 0.5).astype(int)
        x_end = np.ceil(px1 - 0.5).astype(int)

        tc_scan_step = (tcEdgeR - tcEdgeL) / (px1 - px0)[:, None]

        tc = tcEdgeL + tc_scan_step * (x_start + 0.5 - px0)[:, None]

        surf = pygame.surfarray.pixels3d(self.screen)
        tex_surf = pygame.surfarray.pixels3d(texture)
        for i, y in enumerate(range(y_start, y_end)):
            t_pixel = tc[i] + np.arange(0, x_end[i] - x_start[i])[:, None] * tc_scan_step[i]
            t_pixel[:, 0] = t_pixel[:, 0] * tex_width % tex_clamp_x
            t_pixel[:, 1] = t_pixel[:, 1] * tex_height % tex_clamp_y
            t_pixel = t_pixel.astype(int)
            surf[x_start[i]:x_end[i], y] = tex_surf[t_pixel[:, 0], t_pixel[:, 1]]
        del surf
        del tex_surf


    def draw_flat_bottom_textured_triangle(self, v0, v1, v2, texture):
        m0 = (v1[0] - v0[0]) / (v1[1] - v0[1])
        m1 = (v2[0] - v0[0]) / (v2[1] - v0[1])

        y_start = int(np.ceil(v0[1] - 0.5))
        y_end = int(np.ceil(v2[1] - 0.5))

        tcEdgeL = v0[3:].copy()
        tcEdgeR = v0[3:].copy()
        tcBottomL = v1[3:].copy()
        tcBottomR = v2[3:].copy()

        tcEdgeStepL = (tcBottomL - tcEdgeL) / (v1[1] - v0[1])
        tcEdgeStepR = (tcBottomR - tcEdgeR) / (v2[1] - v0[1])

        tcEdgeL += tcEdgeStepL * (y_start + 0.5 - v0[1])
        tcEdgeR += tcEdgeStepR * (y_start + 0.5 - v0[1])
        tcEdgeL = tcEdgeL + np.arange(0, y_end - y_start)[:, None] * tcEdgeStepL
        tcEdgeR = tcEdgeR + np.arange(0, y_end - y_start)[:, None] * tcEdgeStepR

        tex_width = texture.get_width()
        tex_height = texture.get_height()
        tex_clamp_x = tex_width - 1
        tex_clamp_y = tex_height - 1

        px0 = m0 * (np.arange(y_start, y_end) + 0.5 - v0[1]) + v0[0]
        px1 = m1 * (np.arange(y_start, y_end) + 0.5 - v0[1]) + v0[0]

        x_start = np.ceil(px0 - 0.5).astype(int)
        x_end = np.ceil(px1 - 0.5).astype(int)

        tc_scan_step = (tcEdgeR - tcEdgeL) / (px1 - px0)[:, None]

        tc = tcEdgeL + tc_scan_step * (x_start + 0.5 - px0)[:, None]
        surf = pygame.surfarray.pixels3d(self.screen)
        tex_surf = pygame.surfarray.pixels3d(texture)
        for i, y in enumerate(range(y_start, y_end)):
            t_pixel = tc[i] + np.arange(0, x_end[i] - x_start[i])[:, None] * tc_scan_step[i]
            t_pixel[:, 0] = t_pixel[:, 0] * tex_width  % tex_clamp_x
            t_pixel[:, 1] = t_pixel[:, 1] * tex_height % tex_clamp_y
            t_pixel = t_pixel.astype(int)
            surf[x_start[i]:x_end[i], y] = tex_surf[t_pixel[:, 0], t_pixel[:, 1]]
        del surf
        del tex_surf

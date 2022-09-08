import numpy as np
from spaces import CubeScreenTransformer
import pygame
import sys
from copy import copy, deepcopy
from shapes import Vertex
from multiprocess import Process


class Pipeline:
    def __init__(self, gfx, effect, width, height):
        self.gfx = gfx
        self.cst = CubeScreenTransformer(width, height)
        self.effect = effect
        self.Vertex = self.effect.Vertex

    def draw(self, itl):
        vertices = []
        for i in range(len(itl.vertices)):
            vertices.append(self.Vertex(itl.vertices[i, :3], itl.vertices[i, 3:]))
        self.process_vertices(vertices, itl.indices)

    def bind_rotation(self, rotation_in):
        self.rotation = rotation_in

    def bind_translation(self, translation_in):
        self.translation = translation_in

    def bind_texture(self, texture_in):
        self.texture = texture_in
        self.tex_width = self.texture.get_width()
        self.tex_height = self.texture.get_height()
        self.tex_clamp_x = self.tex_width - 1
        self.tex_clamp_y = self.tex_height - 1

    def process_vertices(self, vertices, indices):
        vertices_out = []
        for vertice in vertices:
            vertice.pos = self.rotation.dot(vertice.pos) + self.translation
            vertices_out.append(vertice)
        self.assemble_triangles(deepcopy(vertices_out), indices)

    def assemble_triangles(self, vertices, indices):
        for ind, i in enumerate(indices):
            v0 = vertices[i[0]].pos
            v1 = vertices[i[1]].pos
            v2 = vertices[i[2]].pos
            if np.cross((v1 - v0), (v2 - v0)).dot(v0) <= 0:
                # p = Process(target=self.process_triangle, args=(deepcopy(vertices[i[0]]), deepcopy(vertices[i[1]]),deepcopy(vertices[i[2]]),))
                # p.start()
                self.process_triangle(
                    deepcopy(vertices[i[0]]),
                    deepcopy(vertices[i[1]]),
                    deepcopy(vertices[i[2]]),
                )

    def process_triangle(self, v0, v1, v2):
        self.post_process_triangle_vertices(v0, v1, v2)

    def post_process_triangle_vertices(self, v0, v1, v2):
        v0.pos = self.cst.transform(v0.pos)
        v1.pos = self.cst.transform(v1.pos)
        v2.pos = self.cst.transform(v2.pos)
        self.draw_textured_triangle(v0, v1, v2)

    def draw_textured_triangle(self, v0, v1, v2):
        if v1.pos[1] < v0.pos[1]:
            v0, v1 = v1, v0
        if v2.pos[1] < v1.pos[1]:
            v1, v2 = v2, v1
        if v1.pos[1] < v0.pos[1]:
            v0, v1 = v1, v0
        if v0.pos[1] == v1.pos[1]:
            if v1.pos[0] < v0.pos[0]:
                v0, v1 = v1, v0
            self.draw_flat_top_textured_triangle(v0, v1, v2)
        elif v1.pos[1] == v2.pos[1]:
            if v2.pos[0] < v1.pos[0]:
                v1, v2 = v2, v1
            self.draw_flat_bottom_textured_triangle(v0, v1, v2)

        else:
            alpha_split = (v1.pos[1] - v0.pos[1]) / (v2.pos[1] - v0.pos[1])
            vi = self.gfx.interpolate_to(v0, v2, alpha_split)

            if v1.pos[0] < vi.pos[0]:
                self.draw_flat_bottom_textured_triangle(v0, v1, vi)
                self.draw_flat_top_textured_triangle(v1, vi, v2)

            else:
                self.draw_flat_bottom_textured_triangle(v0, vi, v1)
                self.draw_flat_top_textured_triangle(vi, v1, v2)

    def draw_flat_top_textured_triangle(self, it0, it1, it2):
        delta_y = it2.pos[1] - it0.pos[1]
        dit0 = self.Vertex(it2 - it0) / delta_y
        dit1 = self.Vertex(it2 - it1) / delta_y

        itEdge1 = deepcopy(it1)
        self.draw_flat_textured_triangle(it0, it1, it2, dit0, dit1, itEdge1)

    def draw_flat_bottom_textured_triangle(self, it0, it1, it2):
        delta_y = it2.pos[1] - it0.pos[1]
        dit0 = self.Vertex(it1 - it0) / delta_y
        dit1 = self.Vertex(it2 - it0) / delta_y

        itEdge1 = deepcopy(it0)
        self.draw_flat_textured_triangle(it0, it1, it2, dit0, dit1, itEdge1)

    def draw_flat_textured_triangle(self, it0, it1, it2, dv0, dv1, itEdge1):
        itEdge0 = deepcopy(it0)

        y_start = int(np.ceil(it0.pos[1] - 0.5))
        y_end = int(np.ceil(it2.pos[1] - 0.5))

        itEdge0 += dv0 * (y_start + 0.5 - it0.pos[1])
        itEdge1 += dv1 * (y_start + 0.5 - it0.pos[1])
        itEdge0 = itEdge0.np() + np.arange(0, y_end - y_start)[:, None] * dv0.np()
        itEdge1 = itEdge1.np() + np.arange(0, y_end - y_start)[:, None] * dv1.np()

        x_start = np.ceil(itEdge0[:, 0] - 0.5).astype(int)
        x_end = np.ceil(itEdge1[:, 0] - 0.5).astype(int)

        iLine = itEdge0.copy()
        dx = itEdge1[:, 0] - itEdge0[:, 0]
        diLine = (itEdge1 - iLine) / dx[:, None]

        iLine += diLine * (x_start + 0.5 - itEdge0[:, 0])[:, None]

        surf = pygame.surfarray.pixels3d(self.gfx.screen)
        tex_surf = pygame.surfarray.pixels3d(self.texture)
        for i, y in enumerate(range(y_start, y_end)):
            t_pixel = iLine[i, 3:] + np.arange(0, x_end[i] - x_start[i])[:, None] * diLine[i, 3:]
            surf[x_start[i] : x_end[i], y] = self.effect.ps.pixel(t_pixel)

        del surf
        del tex_surf

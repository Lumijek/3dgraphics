import numpy as np
from spaces import CubeScreenTransformer
import pygame

class Pipeline:
	def __init__(self, gfx, width, height):
		self.gfx = gfx
		self.cst = CubeScreenTransformer(width, height)

	def draw(self, itl):
		self.process_vertices(itl.vertices, itl.indices)

	def bind_rotation(self, rotation_in):
		self.rotation = rotation_in

	def bind_translation(self, translation_in):
		self.translation = translation_in

	def bind_texture(self, texture_in):
		self.texture = texture

	def process_vertices(self, vertices, indices):
		vertices_out = vertices.copy()
		for i, vertice in enumerate(vertices):
			vertices_out[i][:3] = self.rotation.dot(vertice[:3]) + self.translation
		self.assemble_triangles(vertices_out, indices)

	def assemble_triangles(self, vertices, indices):
		for ind, i in enumerate(indices):
			v0 = vertices[i[0]][:3]
			v1 = vertices[i[1]][:3]
			v2 = vertices[i[2]][:3]
			if np.cross((v1 - v0), (v2 - v0)).dot(v0) <= 0:
				self.process_triangle(vertices[i[0]].copy(), vertices[i[1]].copy(), vertices[i[2]].copy())

	def process_triangle(self, v0, v1, v2):
		self.post_process_triangle_vertices(v0, v1, v2)

	def post_process_triangle_vertices(self, v0, v1, v2):
		v0[:3] = self.cst.transform(v0[:3])
		v1[:3] = self.cst.transform(v1[:3])
		v2[:3] = self.cst.transform(v2[:3])
		self.draw_textured_triangle(v0, v1, v2)

	def draw_textured_triangle(self, v0, v1, v2):
		if v1[1] < v0[1]:
			v0, v1 = v1, v0
		if v2[1] < v1[1]:
			v1, v2 = v2, v1
		if v1[1] < v0[1]:
			v0, v1 = v1, v0
		if v0[1] == v1[1]:
			if v1[0] < v0[0]:
				v0, v1 = v1, v0
			self.draw_flat_top_textured_triangle(v0, v1, v2)

		elif v1[1] == v2[1]:
			if v2[0] < v1[0]:
				v1, v2 = v2, v1
			self.draw_flat_bottom_textured_triangle(v0, v1, v2)

		else:
			alpha_split = (v1[1] - v0[1]) / (v2[1] - v0[1])
			vi = self.gfx.interpolate_to(v0, v2, alpha_split)

			if v1[0] < vi[0]:
				self.draw_flat_bottom_textured_triangle(v0, v1, vi)
				self.draw_flat_top_textured_triangle(v1, vi, v2)

			else:
				self.draw_flat_bottom_textured_triangle(v0, vi, v1)
				self.draw_flat_top_textured_triangle(vi, v1, v2)


	def draw_flat_top_textured_triangle(self, v0, v1, v2):
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

		tex_width = self.texture.get_width()
		tex_height = self.texture.get_height()
		tex_clamp_x = tex_width - 1
		tex_clamp_y = tex_height - 1

		px0 = m0 * (np.arange(y_start, y_end) + 0.5 - v0[1]) + v0[0]
		px1 = m1 * (np.arange(y_start, y_end) + 0.5 - v1[1]) + v1[0]

		x_start = np.ceil(px0 - 0.5).astype(int)
		x_end = np.ceil(px1 - 0.5).astype(int)

		tc_scan_step = (tcEdgeR - tcEdgeL) / (px1 - px0)[:, None]

		tc = tcEdgeL + tc_scan_step * (x_start + 0.5 - px0)[:, None]

		surf = pygame.surfarray.pixels3d(self.gfx.screen)
		tex_surf = pygame.surfarray.pixels3d(self.texture)
		for i, y in enumerate(range(y_start, y_end)):
			t_pixel = tc[i] + np.arange(0, x_end[i] - x_start[i])[:, None] * tc_scan_step[i]
			t_pixel[:, 0] = t_pixel[:, 0] * tex_width % tex_clamp_x
			t_pixel[:, 1] = t_pixel[:, 1] * tex_height % tex_clamp_y
			t_pixel = t_pixel.astype(int)
			surf[x_start[i]:x_end[i], y] = tex_surf[t_pixel[:, 0], t_pixel[:, 1]]
		del surf
		del tex_surf

	def draw_flat_bottom_textured_triangle(self, v0, v1, v2):
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

		tex_width = self.texture.get_width()
		tex_height = self.texture.get_height()
		tex_clamp_x = tex_width - 1
		tex_clamp_y = tex_height - 1

		px0 = m0 * (np.arange(y_start, y_end) + 0.5 - v0[1]) + v0[0]
		px1 = m1 * (np.arange(y_start, y_end) + 0.5 - v0[1]) + v0[0]

		x_start = np.ceil(px0 - 0.5).astype(int)
		x_end = np.ceil(px1 - 0.5).astype(int)

		tc_scan_step = (tcEdgeR - tcEdgeL) / (px1 - px0)[:, None]

		tc = tcEdgeL + tc_scan_step * (x_start + 0.5 - px0)[:, None]
		surf = pygame.surfarray.pixels3d(self.gfx.screen)
		tex_surf = pygame.surfarray.pixels3d(self.texture)
		for i, y in enumerate(range(y_start, y_end)):
			t_pixel = tc[i] + np.arange(0, x_end[i] - x_start[i])[:, None] * tc_scan_step[i]
			t_pixel[:, 0] = t_pixel[:, 0] * tex_width  % tex_clamp_x
			t_pixel[:, 1] = t_pixel[:, 1] * tex_height % tex_clamp_y
			t_pixel = t_pixel.astype(int)
			surf[x_start[i]:x_end[i], y] = tex_surf[t_pixel[:, 0], t_pixel[:, 1]]
		del surf
		del tex_surf
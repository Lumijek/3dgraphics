import sys
import time

import numpy as np
import pygame

from graphics import Graphics
from matrix import *
from spaces import CubeScreenTransformer
from shapes import Cube
from pygame.gfxdraw import pixel

WIDTH, HEIGHT = 1000, 1000
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 18, bold=True)
screen.fill("RED")
gfx = Graphics(screen)
cst = CubeScreenTransformer(WIDTH, HEIGHT)
cube = Cube(1, [0, 0, 0])


def wrap_angle(theta):
    modded = np.fmod(theta, 2 * np.pi)
    if modded > np.pi:
        return modded - 2 * np.pi
    else:
        return theta


def fps_counter(screen, clock, font):
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps, 1, pygame.Color("RED"))
    screen.blit(fps_t, (4, 2))

surf = pygame.image.load("images/eye.png").convert_alpha()
surf = pygame.transform.smoothscale(surf, (100, 100))

def compose_frame(screen, cube, theta_x, theta_y, theta_z, offset_z):
    triangles = cube.get_textured_triangles()

    rot_matrix = rotation_x(theta_x) @ rotation_y(theta_y) @ rotation_z(theta_z)

    for i, v in enumerate(triangles.vertices):
        v = rot_matrix.dot(v[:3])
        v += [0, 0, offset_z]
        triangles.vertices[i][:3] = v

    for ind, i in enumerate(triangles.indices):
        v1 = triangles.vertices[i[0]][:3]
        v2 = triangles.vertices[i[1]][:3]
        v3 = triangles.vertices[i[2]][:3]
        triangles.cull_flags[ind] = np.cross((v2 - v1), (v3 - v1)).dot(v1) > 0

    for i, v in enumerate(triangles.vertices):  # transform vertexes to screen space
        triangles.vertices[i][:3] = cst.transform(v[:3])

    for ind, i in enumerate(triangles.indices):
        if not triangles.cull_flags[ind]:
            v1 = triangles.vertices[i[0]]
            v2 = triangles.vertices[i[1]]
            v3 = triangles.vertices[i[2]]
            gfx.draw_textured_triangle(v1, v2, v3, surf)


def main():
    clock = pygame.time.Clock()

    fps = 120
    dt = 1 / fps

    theta = np.pi
    offset_z = 2
    theta_x = 0.0
    theta_y = 0.0
    theta_z = 0.0
    while True:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            theta_x = wrap_angle(theta_x + theta * dt)
        if keys[pygame.K_w]:
            theta_y = wrap_angle(theta_y + theta * dt)
        if keys[pygame.K_e]:
            theta_z = wrap_angle(theta_z + theta * dt)
        if keys[pygame.K_a]:
            theta_x = wrap_angle(theta_x - theta * dt)
        if keys[pygame.K_s]:
            theta_y = wrap_angle(theta_y - theta * dt)
        if keys[pygame.K_d]:
            theta_z = wrap_angle(theta_z - theta * dt)
        if keys[pygame.K_r]:
            offset_z += 2 * dt
        if keys[pygame.K_f]:
            offset_z -= 2 * dt
        screen.fill((0, 0, 0))
        fps_counter(screen, clock, font)

        compose_frame(screen, cube, theta_x, theta_y, theta_z, offset_z)
        pygame.display.update()
        clock.tick(fps)


main()

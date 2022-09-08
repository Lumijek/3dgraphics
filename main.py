import sys
import time

import numpy as np
import pygame

from graphics import Graphics
from matrix import *
import pipeline
from spaces import CubeScreenTransformer
from shapes import Cube, CubeFolded, CubeFoldedWrapped, CubeSkinned
from texture_effect import TextureEffect


WIDTH, HEIGHT = 900, 900
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surf = pygame.image.load("images/dice_skin.png").convert_alpha()
font = pygame.font.SysFont("Arial", 18, bold=True)
gfx = Graphics(screen)
cube = CubeSkinned(1)
te = TextureEffect()
pl = pipeline.Pipeline(gfx, te, WIDTH, HEIGHT)
pl.effect.ps.bind_texture(surf)
pl.bind_texture(surf)


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


def draw(screen, cube, theta_x, theta_y, theta_z, offset_z):
    triangles = cube.get_textured_triangles()
    rot_matrix = rotation_x(theta_x) @ rotation_y(theta_y) @ rotation_z(theta_z)
    pl.bind_rotation(rot_matrix)
    pl.bind_translation([0, 0, offset_z])
    pl.draw(triangles)


def main():
    clock = pygame.time.Clock()

    fps = 240
    dt = 1 / fps

    theta = np.pi
    offset_z = 1.2
    theta_x = 0
    theta_y = 0
    theta_z = 0
    previous_time = time.perf_counter()
    while True:
        dt = time.perf_counter() - previous_time
        previous_time = time.perf_counter()
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

        draw(screen, cube, theta_x, theta_y, theta_z, offset_z)
        pygame.display.update()
        clock.tick(fps)


main()

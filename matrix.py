import numpy as np


def rotation_x(theta):
    sin = np.sin(theta)
    cos = np.cos(theta)

    return np.array([[1, 0, 0], [0, cos, sin], [0, -sin, cos]])


def rotation_y(theta):
    sin = np.sin(theta)
    cos = np.cos(theta)

    return np.array([[cos, 0, -sin], [0, 1, 0], [sin, 0, cos]])


def rotation_z(theta):
    sin = np.sin(theta)
    cos = np.cos(theta)
    return np.array([[cos, sin, 0], [-sin, cos, 0], [0, 0, 1]])

import numpy as np
import pygame
import sys
import math
from pprint import pprint

class Graphics:
    def __init__(self, screen):
        self.screen = screen

    def interpolate(self, src, dest, alpha):
        return src + (dest - src) * alpha

    def interpolate_to(self, src, dest, alpha):
        i1 = self.interpolate(src[:3], dest[:3], alpha)
        i2 = self.interpolate(src[3:], dest[3:], alpha)
        return np.hstack((i1, i2))

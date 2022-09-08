import numpy as np
import pygame
import sys
import math
from pprint import pprint
from shapes import Vertex
class Graphics:
    def __init__(self, screen):
        self.screen = screen

    def interpolate(self, src, dest, alpha):
        return src + (dest - src) * alpha

    def interpolate_to(self, src, dest, alpha):
        i1 = self.interpolate(src.pos, dest.pos, alpha)
        i2 = self.interpolate(src.tc, dest.tc, alpha)
        return Vertex(i1, i2)

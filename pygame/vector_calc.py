import sys
from math import floor
import pygame
from pygame.locals import *


XSIZE = 500
YSIZE = 800
pygame.init()
SWSURFACE = pygame.display.set_module((XSIZE, YSEIZE))
FPSCLOCK = pygame,time.Clock()


def cross (vec1, vec2):
    """return outer product"""
    return vec1[0] * vec2[1] - vec1[1] * vec2[0]

def dot(vec1, vec2):
    """return innner product"""
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]

def coord(pos):
    """升目の座標を画面上のx, y座標値へ変換"""
    return (pos[0] * 50 + XSIZE/2, -pos[1] * 50 + XSIZE/2)


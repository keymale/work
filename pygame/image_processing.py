#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame
from pygame.locals import *

xsize = 500
ysize = 500
pygame.init()
SURFACE = pygame.display.set_mode((xsize, ysize))
FPSCLOCK = pygame.time.Clock()


def process_pixels(data):
    """process pixels"""
    for ypos in range(ysize):
        for xpos in range(xsize):
            val = data[xpos][ypos]
            rval, gval, bval, _ = SURFACE.unmap_rgb(val)
            data[xpos][ypos] = (rval, gval, bval)

def main():
    """mein routine"""
    src = pygame.image.load("c:/Users/keisu/work/pygame/image.png").convert()
    data = pygame.PixelArray(src)
    #process_pixels(data)
    while True:
        for _ in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()
        SURFACE.blit(src, (0, 0))
        pygame.display.update()
        FPSCLOCK.tick(5)
    

if __name__ == "__main__":
    main()


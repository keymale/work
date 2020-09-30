# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import time

grid_num = 8
grid = [[0 for _ in range(grid_num)] for _ in range(grid_num)]


def initialize(width, height, edge, grid):
    pygame.init() # 初期化
    screen = pygame.display.set_mode((width, height)) 
    pygame.display.set_caption("Pygame Test") 
    screen.fill((0,0,0,))
    for w in range(grid_num):
        for h in range(grid_num):
            pygame.draw.rect(screen, (127,255,0), Rect(width // grid_num * w + edge, 
                                                       width // grid_num * h + edge,
                                                       width // grid_num - (2*edge), 
                                                       width // grid_num - (2*edge)))
    grid[3][3] = "B"
    grid[3][4] = "W"
    grid[4][3] = "W"
    grid[4][4] = "B"
    return screen


def update(width, height, edge, grid, screen):
    for w in range(grid_num):
        for h in range(grid_num):
            if grid[h][w] == "B":
                pygame.draw.circle(screen, (5,5,5), (int(width//grid_num*(0.5 + w)),int(width//grid_num*(0.5 + h))),width // grid_num//2 - (edge))
            if grid[h][w] == "W":
                pygame.draw.circle(screen, (250,250,250), (int(width//grid_num*(0.5 + w)),int(width//grid_num*(0.5 + h))),width // grid_num//2 - (edge))
                pygame.draw.circle(screen, (5,5,5), (int(width//grid_num*(0.5 + w)),int(width//grid_num*(0.5 + h))),width // grid_num//2 - (edge),1)

def main():
    width = 600
    height = 700
    edge = 1
    screen = initialize(width, height, edge, grid)
    while(True):
        update(width, height, edge, grid, screen)
        pygame.display.update()

        for event in pygame.event.get(): # 終了処理
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                for w in range(grid_num):
                    for h in range(grid_num):
                        if x > width // grid_num * w + edge and x < width // grid_num * (w + 1) + edge and y > width // grid_num * h + edge and y < width // grid_num * (h + 1) + edge:
                            x_pos = w
                            y_pos = h  
                print(x_pos,y_pos)

def test():
    width = 600
    height = 700
    edge = 1
    pygame.init() # 初期化
    screen = pygame.display.set_mode((width, height)) 
    pygame.display.set_caption("Pygame Test") 
    screen.fill((0,0,0,))
    ball_num = 100
    tx = [0 for _ in range(ball_num)]
    ty = [0 for _ in range(ball_num)]
    tx_d = 1
    ty_d = 1
    speed = 10
    while(True):
        screen.fill((0,0,0,))
        for i in range(ball_num):
            pygame.draw.circle(screen, (127,255,0), (int(tx[i]),int(ty[i])),5)
        if tx[0] >= width:
            tx_d = -1*speed
        elif tx[0] <= 0:
            tx_d = 1*speed
        if ty[0] == height:
            ty_d = -1*speed
        elif ty[0] <= 0:
            ty_d = 1*speed
        tx = [tx[0] + tx_d] + tx[0:ball_num-1]
        ty = [ty[0] + ty_d] + ty[0:ball_num-1]
        pygame.display.update()
        time.sleep(0.1)
            

        for event in pygame.event.get(): # 終了処理
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
if __name__ == "__main__": 
    #main()
    test()
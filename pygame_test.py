# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import time
import numpy as np

class Reversi():
    def __init__(self,w, h, edge, grid_n):
        self.w = w
        self.h = h
        self.edge = edge
        self.grid_n = grid_n
        self.w0 = self.w // self.grid_n
        self.turn = "B"
        self.nextturn = "W"
        self.grid = np.array([['N' for _ in range(self.grid_n + 2)] for _ in range(self.grid_n + 2)])
        pygame.init() # 初期化
        self.font = pygame.font.Font(None, 55)
        self.scr = pygame.display.set_mode((self.w, self.h)) 
        pygame.display.set_caption("Pygame Test") 
        self.grid[4][4] = "B"
        self.grid[4][5] = "W"
        self.grid[5][4] = "W"
        self.grid[5][5] = "B"
        self.update()

    def cnt_piece(self):
        self.cnt_b = np.count_nonzero(self.grid == "B")
        self.cnt_w = np.count_nonzero(self.grid == "W")
        self.cnt_text = self.font.render(str(self.cnt_b) + "(B)VS" + str(self.cnt_w) + "(W)", True, (255,255,255))
        self.scr.blit(self.cnt_text,[self.w/2, self.w])
 
    def update(self):
        '''盤面更新'''
        self.scr.fill((0,0,0,))
        for wi in range(self.grid_n):
            for hi in range(self.grid_n):
                pygame.draw.rect(self.scr,
                                 (127,255,0),
                                 Rect(self.w0 * wi + self.edge, 
                                      self.w0 * hi + self.edge,
                                      self.w0 - (2 * self.edge), 
                                      self.w0 - (2 * self.edge)))
        for wi in range(self.grid_n + 2):
            for hi in range(self.grid_n + 2):
                if self.grid[hi][wi] == "B":
                    pygame.draw.circle(self.scr, (5,5,5), (int(self.w0*(-0.5 + wi)), int(self.w0*(-0.5 + hi))), self.w0//2 - (self.edge))
                if self.grid[hi][wi] == "W":
                    pygame.draw.circle(self.scr, (250,250,250), (int(self.w0*(-0.5 + wi)),int(self.w0*(-0.5 + hi))),self.w0//2 - (self.edge))
                    pygame.draw.circle(self.scr, (5,5,5), (int(self.w0*(-0.5 + wi)),int(self.w0*(-0.5 + hi))), self.w0//2 - (self.edge),1)
        self.cnt_piece()
        pygame.display.update()

    def change_turn(self):
        self.turn, self.nextturn = self.nextturn, self.turn

    def put_enable(self):
        self.en = []
        def check(hi, wi, hi_cnt, wi_cnt):
            hi_cnt0 = hi_cnt
            wi_cnt0 = wi_cnt
            if not self.grid[hi + hi_cnt][wi + wi_cnt] == self.nextturn:
                return False
            else:
                while True:
                    hi_cnt0 += hi_cnt
                    wi_cnt0 += wi_cnt
                    if self.grid[hi + hi_cnt0][wi + wi_cnt0] == "N":
                        return False
                    if self.grid[hi + hi_cnt0][wi + wi_cnt0] == self.turn:
                        self.en.append([hi,wi])
                        return True
        for wi in range(1,self.grid_n + 1):
            for hi in range(1,self.grid_n + 1):
                if self.grid[hi][wi] == "N":
                    for hi_c in [-1, 0, 1]:
                        for wi_c in [-1, 0, 1]:
                            if not(hi_c == 0 and wi_c == 0): 
                                if check(hi, wi, hi_c, wi_c):
                                    break
                        else:
                            continue
                        break
        if self.en == []:
            print("置けるとこないで")
            return False
        else:
            return True

    def return_piece(self, w, h):
        change_piece = []
        self.grid[h][w] = self.turn
        for hi_c in [-1, 0, 1]:
            for wi_c in [-1, 0, 1]:
                hi_c0 = 0
                wi_c0 = 0
                while True:
                    hi_c0 += hi_c
                    wi_c0 += wi_c
                    if self.grid[h + hi_c0][w + wi_c0] == self.nextturn:
                        change_piece.append([h + hi_c0, w + wi_c0])
                        print(change_piece)
                    elif self.grid[h + hi_c0][w + wi_c0] == self.turn:
                        if change_piece == []:
                            break
                        else:
                            for hc, wc in change_piece:
                                self.grid[hc][wc] = self.turn
                            break
                    else:
                        change_piece = []
                        break

    def click2pos(self, click):
        for pos in range(self.grid_n):
            if 0 < click - self.edge -self.w0 * pos < self.w0:
                return pos + 1
    
    def play(self):
        while(True):
            for event in pygame.event.get(): # 終了処理
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    x_pos = self.click2pos(x)
                    y_pos = self.click2pos(y)
                    print("get_posision")
                    if self.put_enable():
                        print("置けます")
                        if [y_pos, x_pos] in self.en:
                            self.return_piece(x_pos, y_pos)
                    else:
                        print("change turn")
                        print(self.turn)
                    self.change_turn()
                    self.update()



def main():
    w = 600
    h = 700
    edge = 1
    grid_n = 8
    reversi = Reversi(w, h, edge, grid_n)
    reversi.play()
    

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
    main()
    #test()

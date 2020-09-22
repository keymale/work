import sys,os
import time
import tkinter as tk
import numpy as np
import random
import copy


class reversi():
    def __init__(self):
        self.row_num = 8
        self.root = tk.Tk()
        self.xsize = 600
        self.ysize = 600
        self.reversi_xsize = 400
        self.reversi_ysize = 400
        self.tagstr = 'abcdefgh'
        self.item_id = 0
        self.pass_check_latch = True
        self.pass_check_latch2 = True
        self.startgame = False
        self.finish = False
        self.judged = False
        self.winner = '△'
        self.p1 = True
        self.p2 = True
        self.turn = '●'
        self.board = [['##' for i in range (self.row_num + 2)] for j in range(self.row_num + 2)]
        self.board[self.row_num//2][self.row_num//2:self.row_num//2+2] =['○','●']
        self.board[self.row_num//2+1][self.row_num//2:self.row_num//2+2] =['●','○']
        self.coordinate = {'x':-1,'y':-1}
        self.dispalay_tk()
            
    def double_check(self,color,board,inputx,inputy):
        if board[inputy][inputx] == '##':
            return True
        else:
            self.display_comment_big('そこはもう置いてあるでしょうが！！！')
            return False
        
    def around_check(self,color,x,y,board):
        empty_cnt = 0
        reversible_cnt = 0
        reversible_tgt = []
        temp_tgt =[]
        pass_flag = False
        for ax in range(x-1,x+2):
            for ay in range(y-1,y+2):
                if ax != x or ay != y:
                    if  board[ay][ax] != '##' and board[ay][ax] != color:
                        empty_cnt += 1
                        temp_tgt += [[ax,ay]]
        if empty_cnt == 0:
            pass_flag = False
        else:
            reversible_tgt_temp = []
            for bx,by in temp_tgt:
                reversible_tgt_temp = [[bx,by]]
                difx = x - bx
                dify = y - by
                temp_reversible_cnt = 1
                cx = bx - difx
                cy = by - dify
                while True:
                    if cx == 0 or cx == self.row_num + 1 or cy == 0 or cy == self.row_num + 1:
                        break
                    elif board[cy][cx] == '##':
                        break
                    elif board[cy][cx] != color:
                        temp_reversible_cnt += 1
                        reversible_tgt_temp += [[cx,cy]]
                    else:
                        reversible_cnt += temp_reversible_cnt
                        reversible_tgt += reversible_tgt_temp
                        pass_flag = True
                        break
                    cx = cx - difx
                    cy = cy - dify
                    
        return pass_flag,reversible_cnt,reversible_tgt
        
    def input_calc(self,color,board,inputx,inputy):
        pass_flag = False
        reversible_tgt_sum = []
        for x in range(1,self.row_num + 1):
            for y in range(1,self.row_num + 1):
                if board[y][x] == '##':
                    pass_check, reversible_cnt,reversible_tgt = self.around_check(color = color, x = x, y = y,board=board)
                    if pass_check:
                        reversible_tgt_sum += reversible_tgt
                        pass_flag = True
        while pass_flag:
            if self.double_check(color = color,board = board,inputx=inputx,inputy=inputy):
                pass_check, reversible_cnt,reversible_tgt = self.around_check(color = color,x = inputx, y = inputy, board = self.board)
                if pass_check:
                    board[inputy][inputx] = color
                    for ax,ay in reversible_tgt:
                        board[ay][ax] = color
                    self.comment.set(str(reversible_cnt) + '個ひっくり返したで')
                    pass_flag = False
                    break
                else:
                    self.display_comment_big('置けまへーん！！')
                    pass_flag = True
                    break
            else:
                pass_flag = True
                break
        return pass_flag,board
    
    def search_enable_place(self,turn,inputx,inputy):
        self.enable_place = []
        self.enable_place_cnt = []
        self.pass_check_latch2 = self.pass_check_latch
        self.pass_check_latch = False
        for x in range(1,self.row_num + 1):
            for y in range(1,self.row_num + 1):
                if self.board[y][x] == '##':
                    pass_check, reversible_cnt,reversible_tgt = self.around_check(color = turn, x = x, y = y,board = self.board)
                    if pass_check:
                        self.enable_place += [[x,y]]
                        self.enable_place_cnt += [[x,y,reversible_cnt]]
                        self.pass_check_latch = True
        ######置くところがないときは自動的にPASS######
        if self.pass_check_latch:
            for  x in list(range(1,self.row_num+1)):
                for y in list(range(1,self.row_num+1)):
                    self.tag = self.tagstr[x-1]+self.tagstr[y-1]
                    self.canvas.create_rectangle(*self.tag_pos[self.tag], fill='green', tags = self.tag)
            for x,y,cnt in self.enable_place_cnt:
                self.tag = self.tagstr[x-1]+self.tagstr[y-1]
                self.canvas.create_rectangle(*self.tag_pos[self.tag], fill='green2', tags = self.tag)
            return True
        else:
            if self.pass_check_latch2:
                self.turn = self.change_turn(turn) 
                self.display_comment_big('もう置くとこないからPASSやな!' + self.turn + 'の番です')
                return False
            else:
                self.finish = True
                return self.judge()
                
    def judge(self):
        cnt_b,cnt_w = self.cnt_board()
        if cnt_b > cnt_w:
            self.winner = '●'
        elif cnt_b < cnt_w:
            self.winner = '○'
        else:
            self.display_comment_big('終わりでーす!引き分け！')
            return True
        self.display_comment_big('終わりでーす!'+self.winner+'の勝ちやで！')
        return True
        
    def change_turn(self,turn):
        if turn == '●':
            return '○'
        else:
            return '●'
        
    def pos2tag(self, pos):
        for p, t in zip(list(range(1,self.row_num+1)),self.tagstr):
            if pos == p : 
                return t
            
    def tag2pos(self, tag):
        for p, t in zip(list(range(1,self.row_num+1)),self.tagstr):
            if tag == t : 
                return p
            
    def refresh_board(self):
        for x in range(1,self.row_num+1):
            for y in range(1,self.row_num+1):
                self.tag = self.tagstr[x-1]+self.tagstr[y-1]
                if self.board[y][x] == '●':
                    self.canvas.create_oval(*self.tag_pos[self.tag], fill='black',tags = self.tag)
                elif self.board[y][x] =='○':
                    self.canvas.create_oval(*self.tag_pos[self.tag], fill='white',tags = self.tag)
                    
    
    def cnt_board(self):
        cnt_b = 0
        cnt_w = 0
        for i in range(1,self.row_num+1):
            cnt_b += self.board[i].count('●')
            cnt_w += self.board[i].count('○')
        return cnt_b, cnt_w
    
    def display_comment(self):
        cnt_b,cnt_w = self.cnt_board()
        Static2 = tk.Label(textvariable=self.comment)
        self.cnt_bw.set('● : ○ = '+str(cnt_b)+' : '+str(cnt_w))
        Static_cntbw = tk.Label(textvariable=self.cnt_bw)
        Static2.place(x=self.xsize/2-200, y=self.ysize -65)
        Static_cntbw.place(x=self.xsize/2, y=self.ysize -90)
    
    def display_comment_big(self,comment):
        Static1 = tk.Label(text = comment, font=("",20),bg='white')
        Static1.place(x=0,
                      y=0,
                      width=self.xsize,
                      height=100)
        return Static1
    
    def update(self):
        pass_flag, self.board = self.input_calc(color = self.turn, board = self.board,inputx = self.coordinate['x'],inputy = self.coordinate['y'])
        if not pass_flag:
            self.turn = self.change_turn(self.turn)
        while not self.search_enable_place(turn=self.turn,inputx=self.coordinate['x'],inputy=self.coordinate['y']):
            pass
        self.refresh_board()
        self.display_comment()
        if ((not self.p2) and (self.turn == '○'))or((not self.p1) and (self.turn == '●')): 
            self.display_comment_big(self.turn + 'の番です(CPU)')
        else:
            self.display_comment_big(self.turn + 'の番です')
    
    def pvp(self):
        self.p1,self.p2 = True, True
        self.aft_push_strt_btn()
        
    def pvc(self):
        self.p1,self.p2 = True, False
        self.aft_push_strt_btn()
    
    def cvp(self):
        self.p1,self.p2 = False, True
        self.aft_push_strt_btn()
    
    def cvc(self):
        self.p1,self.p2 = False, False
        self.aft_push_strt_btn()
        
    def aft_push_strt_btn(self):
        self.startgame = True
        self.startfrm.pack_forget()
        while not self.search_enable_place(turn=self.turn,inputx=self.coordinate['x'],inputy=self.coordinate['y']):
            pass
        self.refresh_board()
        if ((not self.p2) and (self.turn == '○'))or((not self.p1) and (self.turn == '●')): 
            self.display_comment_big(self.turn + 'の番です(CPU)')
        else:
            self.display_comment_big(self.turn + 'の番です')
        
#オセロの盤面を押したときのファンクション        
    def pressed(self,event):
        self.item_id = self.canvas.find_closest(event.x, event.y)
        self.tag = self.canvas.gettags(self.item_id[0])[0]
        self.coordinate['x'] = self.tag2pos(self.tag[0])
        self.coordinate['y'] = self.tag2pos(self.tag[1])
        self.update()

#CPUの動作
    def cpu_lv1(self):
        change_cnt_max = 0
        cm_x = 0
        cm_y = 0
        for x, y, cnt in self.enable_place_cnt:
            if change_cnt_max < cnt:
                change_cnt_max = cnt
                cm_x = x
                cm_y = y
            elif change_cnt_max == cnt:
                temp = random.randint(0,2)
                if temp == 0:
                    cm_x = x
                    cm_y = y
        self.coordinate['x'] = x
        self.coordinate['y'] = y
            
    def cpu_lv2(self):
        change_cnt_max = 0
        cm_x = 0
        cm_y = 0
        kado =  [[1,1], [1,8], [8,1], [8,8]]
        kado_near = [[1,2],[1,7],[2,1],[2,2],[2,7],[2,8],[7,1],[7,2],[7,7],[7,8],[8,2],[8,7]]
        opponent_enable_put_num = 0
        e_p_c = 0
        temp_turn = self.change_turn(self.turn)
        for ax, ay, acnt in self.enable_place_cnt:
            kado_flag = False
            original_board = copy.deepcopy(self.board)
            pass_flag, temp_board = self.input_calc(color = self.turn, board = original_board,inputx = ax,inputy = ay)
            p_c, r_c,r_t = self.around_check(color = self.turn, x = ax, y = ay,board = temp_board)
            enable_place = []
            enable_place_cnt = []
            for bx in range(1,self.row_num + 1):
                for by in range(1,self.row_num + 1):
                    if temp_board[by][bx] == '##':
                        pass_check, reversible_cnt,reversible_tgt = self.around_check(color = temp_turn, x = bx, y = by,board = temp_board)
                        if pass_check:
                            bxy = [bx,by]
                            if not (bxy in kado):
                                enable_place += [[bx,by]]
                                enable_place_cnt += [[bx,by,reversible_cnt]]
                            elif not ((bx in [1,8]) or (by in [1,8])):
                                enable_place += [[bx,by]]
                                enable_place_cnt += [[bx,by,reversible_cnt]]
                            else :
                                print(bxy)
                                kado_flag = True
            if not kado_flag:
                if [ax,ay] in  kado:
                    cm_x = ax
                    cm_y = ay
                    break
                if [ax,ay] in kado_near:
                    pass
                elif (ax in [1,8]):
                    if self.board[ay - 1][ax] == '##' and self.board[ay + 1][ax] == '##':
                        cm_x = ax
                        cm_y = ay
                        break
                    elif ay in [3,6]:
                        cm_x = ax
                        cm_y = ay
                        break
                    elif ay == 4:
                        if self.board[ay - 1][ax] == self.turn:
                            cm_x = ax
                            cm_y = ay
                            break
                        elif self.board[ay + 2][ax] == self.turn and self.board[ay + 1][ax] == self.change_turn(self.turn):
                            cm_x = ax
                            cm_y = ay
                            break
                    elif ay == 5:
                        if self.board[ay + 1][ax] == self.turn:
                            cm_x = ax
                            cm_y = ay
                            break
                        elif self.board[ay - 2][ax] == self.turn and self.board[ay - 1][ax] == self.change_turn(self.turn):
                            cm_x = ax
                            cm_y = ay
                            break
                elif (ay in [1,8]):
                    if self.board[ay][ax - 1] == '##' and self.board[ay][ax+1] == '##':
                        cm_x = ax
                        cm_y = ay
                        break
                    elif ax in [3,6]:
                        cm_x = ax
                        cm_y = ay
                        break
                    elif ax == 4:
                        if self.board[ay][ax - 1] == self.turn:
                            cm_x = ax
                            cm_y = ay
                            break
                        elif self.board[ay][ax + 2] == self.turn and self.board[ay][ax + 1] == self.change_turn(self.turn):
                            cm_x = ax
                            cm_y = ay
                            break
                    elif ax == 5:
                        if self.board[ay][ax + 1] == self.turn:
                            cm_x = ax
                            cm_y = ay
                            break
                        elif self.board[ay][ax - 2] == self.turn and self.board[ay][ax - 1] == self.change_turn(self.turn):
                            cm_x = ax
                            cm_y = ay
                            break
                elif opponent_enable_put_num < len(enable_place):
                    cm_x = ax
                    cm_y = ay
                    opponent_enable_place = enable_place
                    opponent_enable_put_num = len(enable_place)
                    enable_place_cnt = r_c
                elif opponent_enable_put_num == len(enable_place):
                    if e_p_c < r_c:
                        cm_x = ax
                        cm_y = ay
                        e_p_c = r_c
                        opponent_enable_place = enable_place
        print(cm_x,cm_y)
        print(enable_place)
        if cm_x == 0 or cm_y == 0:
            self.cpu_lv1()
        else:
            self.coordinate['x'] = cm_x
            self.coordinate['y'] = cm_y
            
    def dispalay_tk(self):
        self.comment = tk.StringVar()
        self.cnt_bw = tk.StringVar()
        self.comment.set('楽しい楽しいオセロの始まりやで')
        xedge = (self.xsize - self.reversi_xsize)/2
        yedge = (self.ysize - self.reversi_ysize)/2
        self.startfrm = tk.Frame(self.root)
        for name, command in zip (['pvp','pvc','cvp','cvc'],[self.pvp,self.pvc,self.cvp,self.cvc]):
            tk.Button(self.startfrm, text = name, command = command,width = 10).pack()#fill = tk.LEFT)
        self.startfrm.pack(fill = tk.BOTH)
        self.root.title("リバーシ")
        self.root.minsize(self.xsize, self.ysize)
        self.canvas = tk.Canvas(bg="green", width=self.reversi_xsize, height=self.reversi_ysize)
        self.canvas.place(x=xedge,y=yedge)
        self.tag_pos = {}
        for  xstr,x in zip(self.tagstr,list(range(1,self.row_num+1))):
            for ystr,y in zip(self.tagstr,list(range(1,self.row_num+1))):
                self.tag = xstr + ystr
                self.tag_pos[self.tag] = (x-1)*(self.reversi_ysize/(self.row_num)), (y-1)*(self.reversi_ysize/(self.row_num)), x*(self.reversi_ysize/(self.row_num)), y*(self.reversi_ysize/(self.row_num)),
                self.canvas.create_rectangle(*self.tag_pos[self.tag], fill='green', tags = self.tag)
                self.canvas.tag_bind(self.tag, "<ButtonPress-1>", self.pressed)
        self.run_display()
        self.refresh_board()
        self.display_comment_big(self.turn + 'の番です')
    

    def run_display(self):
        while True:
            self.root.update_idletasks()
            self.root.update()
            if self.finish:
                if self.judged:
                    pass
                else:
                    self.judged = self.judge()
            else:
                if ((not self.p2) and (self.turn == '○'))or((not self.p1) and (self.turn == '●')): 
                    self.cpu_lv2()
                    self.root.after(100,self.update())
        pass


if __name__ == "__main__":
    reversi = reversi()
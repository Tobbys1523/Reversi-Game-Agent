import random
import pygame
import sys
from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION
from reversi import Reversi
import time

class BaseAgent():
    def __init__(self, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):
        self.color = color
        self.rows_n = rows_n
        self.cols_n = cols_n
        self.block_len = 0.8 * min(height, width)/cols_n
        self.col_offset = (width - height)/2 + 0.1 * min(height, width) + 0.5 * self.block_len
        self.row_offset = 0.1 * min(height, width) + 0.5 * self.block_len
        

    def step(self, reward, obs):
        """
        Parameters
        ----------
        reward : dict
            current_score - previous_score
            
            key: -1(black), 1(white)
            value: numbers
            
        obs    :  dict 
            board status

            key: int 0 ~ 63
            value: [-1, 0 ,1]
                    -1 : black
                     0 : empty
                     1 : white

        Returns
        -------
        tuple:
            (x, y) represents position, where (0, 0) mean top left. 
                x: go right
                y: go down
        event_type:
            non human agent uses pygame.USEREVENT
        """

        raise NotImplementError("You didn't finish your step function. Please override step function of BaseAgent!")
    
class HumanAgent(BaseAgent):
    def step(self, reward, obs):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                return event.pos, event.type
            if event.type == pygame.MOUSEBUTTONDOWN:
                return event.pos, pygame.USEREVENT

        return (-1, -1), None



class RandomAgent(BaseAgent):
    #改成從可下步伐中隨機抽出
    def step(self, reward, obs):
        move = []
        for i in range(64):
            can = self.can_place(obs,i,self.color)
            if can ==True:
                move.append(i)
        p = random.randint(0,len(move)-1)
        return (self.col_offset + (move[p]%8) * self.block_len, self.row_offset + (move[p]//8) * self.block_len), pygame.USEREVENT

    
    def can_place(self,obs,place,color):
        '''
        確認周遭九宮格中是否有敵手的旗子

        Parameter
        ------------------------
        obs : dict
        棋盤戰況

        place : int
        要測試是否能放的點

        color : str
        我方顏色

        '''
        if obs[place]!=0:
            return False
        x=place%8
        y=place//8
        sc=1
        if color == 'black': 
            sc = -1
        is_avail = False
        for i in range(-1, 2):
            if x+i < 0 or x+i > 7: continue
            for j in range(-1, 2):
                if y+j < 0 or y+j > 7: continue
                if obs[x+i+(y+j)*8] == -1 * sc:
                    if self.check_direction(x, y, i, j,obs,sc):
                        is_avail = True
        return is_avail
    
    def check_direction(self,row,col,dx,dy,obs,sc,flip=False):
        '''
        測試輸入點在輸入方向是否有我方旗子一同夾住敵手旗子

        Parameter
        ------------------------
        row : int
        測試點x軸

        col : int
        測試點y軸

        dx : int
        測試方向x分量

        dy : int
        測試方向y分量

        obs : dict
        棋盤戰況

        sc : int 
        我方顏色代碼
        -1 : black
         1 : white
        '''
        is_avail = False
        x, y = [dx], [dy]
        while 0 <= row+x[-1] < 8 and 0 <= col+y[-1] < 8:
            label = row+x[-1]+8*(col+y[-1])
            if obs[label]==0:
                break
            if obs[label] == sc:
                return True
            x.append(x[-1] + dx)
            y.append(y[-1] + dy)
        return is_avail


'''
-------------------------------------------------------
old random write by TA
-------------------------------------------------------
class RandomAgent(BaseAgent):
    def step(self, reward, obs):
        
        return (self.col_offset + random.randint(0, self.cols_n-1) * self.block_len, self.row_offset + random.randint(0, self.rows_n-1) * self.block_len), pygame.USEREVENT
   '''     
class MyAgent(BaseAgent):
    def step(self, reward, obs):
        move = []
        k={}
        sc,maxi,maxii = 1,0,0
        if self.color == 'black': 
            sc = -1
        for i in range(64):
            can = self.can_place(obs,i,sc)
            if can ==True:
                move.append(i)
        for i in move:
            k = self.flip_or_not(i%8,i//8,obs,sc)
            ans = self.how_many(k,sc)
            if ans>maxi:
                maxi=ans
                maxii=i
        return (self.col_offset + (maxii%8) * self.block_len, self.row_offset + (maxii//8) * self.block_len), pygame.USEREVENT

    def flip_or_not(self,x,y,obs,sc):
        ans = obs.copy()
        for i in range(-1, 2):
            if x+i < 0 or x+i > 7: continue
            for j in range(-1, 2):
                if y+j < 0 or y+j > 7: continue
                if obs[x+i+(y+j)*8] == -1 * sc:
                    ans = self.flip_it(x, y, i, j,ans,sc)
        return ans
                        
        
    def can_place(self,obs,place,sc):
        '''
        確認周遭九宮格中是否有敵手的旗子

        Parameter
        ------------------------
        obs : dict
        棋盤戰況

        place : int
        要測試是否能放的點

        color : str
        我方顏色

        '''
        if obs[place]!=0:
            return False
        x=place%8
        y=place//8
        is_avail = False
        for i in range(-1, 2):
            if x+i < 0 or x+i > 7: continue
            for j in range(-1, 2):
                if y+j < 0 or y+j > 7: continue
                if obs[x+i+(y+j)*8] == -1 * sc:
                    if self.check_direction(x, y, i, j,obs,sc):
                        is_avail = True
        return is_avail
    
    def check_direction(self,row,col,dx,dy,obs,sc,flip=False):
        '''
        測試輸入點在輸入方向是否有我方旗子一同夾住敵手旗子

        Parameter
        ------------------------
        row : int
        測試點x軸

        col : int
        測試點y軸

        dx : int
        測試方向x分量

        dy : int
        測試方向y分量

        obs : dict
        棋盤戰況

        sc : int 
        我方顏色代碼
        -1 : black
         1 : white
        '''
        is_avail = False
        x, y = [dx], [dy]
        while 0 <= row+x[-1] < 8 and 0 <= col+y[-1] < 8:
            label = row+x[-1]+8*(col+y[-1])
            if obs[label]==0:
                break
            if obs[label] == sc:
                if flip:
                    ans = obs.copy()
                    for r, c in zip(x, y):
                        ans[row+r+8*(col+c)]=sc
                    return ans
                return True
            x.append(x[-1] + dx)
            y.append(y[-1] + dy)
        return is_avail

    def how_many(self,want,sc):
        k=0
        for i in range(64):
            if want[i]==sc:
                k+=1
        return k

    def flip_it(self,row,col,dx,dy,obs,sc):

        ans = obs.copy()
        x, y = [dx], [dy]
        while 0 <= row+x[-1] < 8 and 0 <= col+y[-1] < 8:
            label = row+x[-1]+8*(col+y[-1])
            if obs[label]==0:
                break
            if obs[label] == sc:
                for r, c in zip(x, y):
                    ans[row+r+8*(col+c)]=sc
                return ans
            x.append(x[-1] + dx)
            y.append(y[-1] + dy)
        return ans

if __name__ == "__main__":
    agent = RandomAgent()
    print(agent.step(None, None))

import time
from Arguments import *


class AI_player:
    def __init__(self, num, ball, walls, fireballs, humans, meteors):
        self.number = num
        self.ball = ball
        self.walls = walls
        self.fireballs = fireballs
        self.humans = humans
        self.meteors = meteors

    def refresh(self, ball, walls, fireballs, humans, meteors):
        self.ball = ball
        self.walls = walls
        self.fireballs = fireballs
        self.humans = humans
        self.meteors = meteors

    def analysis(self):
        ans = (0, 0, 0)
        return ans
        # do something
        # 返回的三个数(flag,x,y)表示如下含义
        # flag==1 向前移动x距离
        # flag==2 旋转x角度
        # flag==3 向前发射一颗火球
        # flag==4 在(x,y)处使用一次天降正义
        # 每次只能选择一个操作
        # 旋转角最大为±human_rotate_max，前后距离最大为±human_speed_max


class Time_Out_AI_player:
    def __init__(self, num, ball, walls, fireballs, humans, meteors):
        self.number = num
        self.ball = ball
        self.walls = walls
        self.fireballs = fireballs
        self.humans = humans
        self.meteors = meteors

    def refresh(self, ball, walls, fireballs, humans, meteors):
        self.ball = ball
        self.walls = walls
        self.fireballs = fireballs
        self.humans = humans
        self.meteors = meteors

    def analysis(self):
        ans = (2, human_rotate_max, 0)
        time.sleep(1)
        return ans
        # do something
        # 返回的三个数(flag,x,y)表示如下含义
        # flag==1 向前移动x距离
        # flag==2 旋转x角度
        # flag==3 向前发射一颗火球
        # flag==4 在(x,y)处使用一次天降正义
        # 每次只能选择一个操作
        # 旋转角最大为±human_rotate_max，前后距离最大为±human_speed_max

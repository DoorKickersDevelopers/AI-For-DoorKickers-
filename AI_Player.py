import time
from Arguments import *
from math import cos, sin, pi
import random


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
        tmp = random.randint(1, 10)
        if tmp > 9:
            ans = (2, -10, 0)
        elif tmp > 8:
            ans = (2, 10, 0)
        elif tmp > 5:
            ans = (4, self.humans[self.number].circle.centre.x,
                   self.humans[self.number].circle.centre.y)
        elif tmp > 2:
            ans = (3, 0, 0)
        else:
            dx = human_speed_max * cos(2 * random.random() * pi)
            dy = human_speed_max * sin(2 * random.random() * pi)
            dx += self.humans[self.number].circle.centre.x
            dy += self.humans[self.number].circle.centre.y
            ans = (1, dx, dy)
        return ans

        # do something
        # 返回的三个数(flag,x,y)表示如下含义
        # flag==1 移动到(x,y)位置
        # flag==2 旋转x角度
        # flag==3 向前发射一颗火球
        # flag==4 在(x,y)处使用一次天降正义
        # 每次只能选择一个操作
        # 旋转角最大为±human_rotate_max L2Distance((x,y),position)<=human_speed_max


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

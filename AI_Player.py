class AI_player:
    def __init__(self, num, ball, wall, bul, human, gre):
        self.number = num
        self.ball = ball
        self.wall = wall
        self.bullets = bul
        self.humans = human
        self.grenades = gre

    def getdata(self, num, ball, wall, bul, human, gre):
        self.number = num
        self.ball = ball
        self.wall = wall
        self.bullets = bul
        self.humans = human
        self.grenades = gre

    def analysis(self):
        a = self.num
        ans = (0, 0, 0, False, False)
        return ans
        # do something
        # 返回值的五个数分别为：操作类型（为1,2,3,4,与后面一一对应），旋转角度，前后移动距离，是否开火，是否扔手榴弹
        # 每次只能选择一个操作
        # 旋转角最大为±human_rotate_max，前后距离最大为±human_speed_max
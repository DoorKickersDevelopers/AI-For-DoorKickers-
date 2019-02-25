PYGAME = False
DEBUG = False
if PYGAME:
    import pygame
    from pygame import Rect
import sys
import random
import copy
import time
from AI_Player import *
import threading
from Arguments import *
from BaseClass import *
from MySTL import *
from multiprocessing import Pool
import json
import logging
import numpy as np
import pandas as pd


BYTEORDER = 'big'

width = int(width_of_screen / room_size)
height = int(height_of_screen / room_size)
width_offset = 1.0 * (width_of_screen - room_size * width) / 2
height_offset = 1.0 * (height_of_screen - room_size * height) / 2


def GenerateMap():

    Map = np.random.randint(0, 1000, (width, height))
    Map = Map < 1000 * density_of_wall

    cnt = np.zeros((width, height), dtype=np.int32)
    cnt2 = cnt.copy()

    def count1(i, j):
        lx = max(i - 1, 0)
        rx = min(i + 2, width)
        ly = max(j - 1, 0)
        ry = min(j + 2, height)
        ans = 9 - (~Map[lx:rx, ly:ry]).sum()
        return ans

    def count2(i, j):
        lx = max(i - 2, 0)
        rx = min(i + 3, width)
        ly = max(j - 2, 0)
        ry = min(j + 3, height)
        ans = 25 - (~Map[lx:rx, ly:ry]).sum()
        return ans

    for Round in range(4):
        for i in range(width):
            for j in range(height):
                cnt[i, j] = count1(i, j)
        for i in range(width):
            for j in range(height):
                cnt2[i, j] = count2(i, j)
        Map = (cnt >= 5) | (cnt2 - cnt <= 2)

    for Round in range(3):
        for i in range(width):
            for j in range(height):
                cnt[i, j] = count1(i, j)
        Map = cnt >= 5
    return Map


def bfs(stx, sty, Map):
    Flag = Map[stx, sty]
    color = np.zeros((width, height), dtype=np.bool)
    color[stx][sty] = True
    dxs = [-1, 1, 0, 0]
    dys = [0, 0, -1, 1]

    queue = [(stx, sty)]

    while queue != []:
        x, y = queue.pop(0)
        for dx, dy in zip(dxs, dys):
            if 0 <= x + dx and x + dx < width and 0 <= y + dy and y + dy < height and (Map[x + dx, y + dy] == Flag) and (not color[x + dx][y + dy]):
                color[x + dx][y + dy] = True
                queue.append((x + dx, y + dy))
    return color


def check(Map):

    for i in range(width):
        for j in range(height):
            if (not Map[i, j]):
                color = bfs(i, j, Map)
                break
        else:
            continue
        break

    if ((~Map) & (~color)).any():
        return False

    if Map.sum() > width * height * (density_of_wall + 0.2):
        return False

    return True


StartPoints = []


def Init(human_number, log):
    Map = GenerateMap()

    while not check(Map):
        if DEBUG:
            print("Generate Map Failed")
        Map = GenerateMap()

    if DEBUG:
        print("-----------------Game Map-----------------")
        print()
        for i in range(width):
            for j in range(height):
                if(Map[i, j]):
                    print("O", end='')
                else:
                    print("*", end='')
            print()
        print("-----------------        -----------------")

    RealMap = np.zeros((width, height), dtype=np.bool)

    def GetReachPoints(x, y):
        ReachPoints = [(x, y)]
        queue = [(x, y)]
        color = np.zeros((width, height), dtype=np.bool)
        color[x, y] = True
        dxs = [-1, 1, 0, 0]
        dys = [0, 0, -1, 1]
        while queue != []:
            x, y = queue.pop(0)
            for dx, dy in zip(dxs, dys):
                if 0 <= x + dx and x + dx < width and 0 <= y + dy and y + dy < height and (Map[x + dx][y + dy]) and (not color[x + dx][y + dy]):
                    color[x + dx, y + dy] = True
                    queue.append((x + dx, y + dy))
                    ReachPoints.append((x + dx, y + dy))
        return ReachPoints

    walls = []

    rightest = np.zeros((width, height), dtype=np.int32)

    ans = Map.sum()

    for Round in range(max_num_of_wall):
        if ans == 0:
            break
        for j in range(height):
            for i in range(width - 1, -1, -1):
                if not Map[i, j]:
                    continue
                if i == width - 1:
                    rightest[i, j] = i
                else:
                    if Map[i + 1, j]:
                        rightest[i, j] = rightest[i + 1, j]
                    else:
                        rightest[i, j] = i

        ansx1, ansx2, ansy1, ansy2 = 0, -1, 0, -1

        WallPos = []
        for x in range(width):
            for y in range(height):
                if Map[x, y]:
                    WallPos.append((x, y))
        assert(len(WallPos) == ans)
        x, y = WallPos[random.randint(0, len(WallPos) - 1)]
        # 选取该联通块，使用面积最大的矩形覆盖
        ReachPoints = GetReachPoints(x, y)
        for x, y in ReachPoints:
            assert(Map[x][y] == True)
            # left bottom point
            right = width
            for yy in range(y, height):
                if not Map[x, yy]:
                    break
                right = min(right, rightest[x, yy])
                x1, x2, y1, y2 = x, right, y, yy
                if (x2 - x1 + 1) * (y2 - y1 + 1) > (ansx2 - ansx1 + 1) * (ansy2 - ansy1 + 1):
                    ansx1, ansx2, ansy1, ansy2 = x1, x2, y1, y2
        RealMap[ansx1:ansx2 + 1, ansy1:ansy2 + 1] = True
        Map[ansx1:ansx2 + 1, ansy1:ansy2 + 1] = False

        ans -= (ansx2 - ansx1 + 1) * (ansy2 - ansy1 + 1)
        ansx1 = width_offset + ansx1 * room_size
        ansx2 = width_offset + (ansx2 + 1) * room_size
        ansy1 = height_offset + ansy1 * room_size
        ansy2 = height_offset + (ansy2 + 1) * room_size

        walls.append(Wall(ansx1, ansx2, ansy1, ansy2))
    if DEBUG:
        print("-----------------Real Map-----------------")
        print()
        for i in range(width):
            for j in range(height):
                if(RealMap[i, j]):
                    print("O", end='')
                else:
                    print("*", end='')
            print()
        print("-----------------        -----------------")

    global StartPoints

    for x in range(width):
        for y in range(height):
            if not RealMap[x][y]:
                StartPoints.append(
                    (width_offset + (x + 0.5) * room_size, height_offset + (y + 0.5) * room_size))

    StartPoints = pd.Series(StartPoints)

    poss = StartPoints.sample(n=human_number + 1)

    ball_x, ball_y = poss.iloc[0]

    ball = Ball(Point(ball_x, ball_y))

    humans = []

    for i in range(human_number):
        x, y = poss.iloc[i + 1]
        rot = random.randint(0, 359)
        humans.append(Human(Point(x, y), rot, i))

    log["walls"] = str(walls)

    return walls, humans, ball


def update_ball(ball, humans, eventlist):
    if ball.belong !=-1:
        ball.circle.centre = humans[ball.belong].circle.centre
    else:
        for human in humans:
            if (human is not None) and CircleIntersection(ball.circle, human.circle):
                ball.belong = human.number
                eventlist.append([5, human.number])
                ball.circle.centre = human.circle.centre

def move(human, x,y, walls):
    if L2Distance(Point(x,y),human.circle.centre)>eps+human_speed_max:
        x,y = human.circle.centre.x,human.circle.centre.y
    if HumanCanGotoPos(human,walls,Point(x,y)):
        human.circle.centre = Point(x,y)


def shoot(human, fireballs, walls):
    if human.attack_time == 0:
        human.attack_time = human.fireball_interval
        p = MoveAlongAngle(human.circle.centre, human.rotation,
                           human_radius + fireball_radius)
        if LegalPos(Circle(p, fireball_radius), walls):
            fireballs.append(Fireball(p, human.rotation))
            return True
    return False


def rotate(human, angle):
    if abs(angle) > human_rotate_max:
        if angle > 0:
            angle = human_rotate_max
        else:
            angle = -human_rotate_max

    human.rotation += angle
    if human.rotation < 0:
        human.rotation += 360
    elif human.rotation >= 360:
        human.rotation -= 360


def throw(human, meteors, pos, walls):
    if human.attack_time == 0 and human.meteor_number > 0:
        if 0 <= pos.x and pos.x <= width_of_screen and 0 <= pos.y and pos.y <= height_of_screen and L2Distance(pos, human.circle.centre) <= human.meteor_cast_distance:
            human.meteor_number -= 1
            human.attack_time = human.meteor_interval
            meteors.append(Meteor(pos))
            return True
    return False


logs = []


def sendLog(log, Type=0, UserCode=-1):
    if DEBUG:
        print("~~~~~~~~~~~~~~~~~~~Send Msg~~~~~~~~~~~~~~~~~~~")
        print("Type=", Type, "UserCode", UserCode)
        print(log)
        print("~~~~~~~~~~~~~~~~~~~        ~~~~~~~~~~~~~~~~~~~")
        return
    Body = json.dumps(log).encode()
    if UserCode == -1:
        logs.append(log)
    if Type == 2:
        Len = len(Body) + 4
        toSend = Len.to_bytes(4, byteorder=BYTEORDER, signed=True)
        toSend += Type.to_bytes(4, byteorder=BYTEORDER, signed=True)
        toSend += Body
        sys.stdout.buffer.write(toSend)
        sys.stdout.flush()
    else:
        Len = len(Body) + 8
        toSend = Len.to_bytes(4, byteorder=BYTEORDER, signed=True)
        toSend += Type.to_bytes(4, byteorder=BYTEORDER, signed=True)
        toSend += UserCode.to_bytes(4, byteorder=BYTEORDER, signed=True)
        toSend += Body
        sys.stdout.buffer.write(toSend)
        sys.stdout.flush()


class Listen(threading.Thread):
    def __init__(self, human_number):
        super(Listen, self).__init__()
        self.human_number = human_number
        self.ans = {}
        #self.state = True
        for i in range(human_number):
            self.ans[i] = (0, 0, 0)

    def recvData(self):
        Len = int.from_bytes(sys.stdin.buffer.read(
            4), byteorder=BYTEORDER, signed=True)
        # print("*******************************************************************\n\n\n\n\n\n")
        Type = int.from_bytes(sys.stdin.buffer.read(
            4), byteorder=BYTEORDER, signed=True)
        UserCode = int.from_bytes(sys.stdin.buffer.read(
            4), byteorder=BYTEORDER, signed=True)
        if Type == 0:  # 用户AI发送的包
            tmp = str(sys.stdin.buffer.read(Len - 8), 'utf-8')
            # data = json.loads(str(sys.stdin.buffer.read(Len-8), 'utf-8')) # 读取主体部分
            # data = json.loads(str(sys.stdin.buffer.read(Len), 'utf-8')) # 读取主体部分
            data = json.loads(tmp)  # 读取主体部分

            # zaizheli
            #sendLog(data, 0, -1)
            #

            if UserCode in self.ans.keys():
                #if DEBUG:
                #    print("~~~~~~~~~~~~~~~~~~~Recv Msg~~~~~~~~~~~~~~~~~~~")
                #    print('AI:', UserCode, data)  # debug
                #    print("~~~~~~~~~~~~~~~~~~~        ~~~~~~~~~~~~~~~~~~~")
                self.ans[UserCode] = (data["flag"],data["args"][0],data["args"][1])  # 更新对象状态
                if self.ans[UserCode][0]==5:
                    return False
                #sendLog(data,0,-1)
                # self.gameProcess(UserCode)  # 在状态变更后进行游戏逻辑处理
                # self.sendData({'received':True}, 0, UserCode)
            return True

    def run(self):
        while True:
            # if not self.state:
            #    return
            if not self.recvData():
                break

if PYGAME:
    def draw_rectangle(screen, rect, color):
        pygame.draw.rect(screen, color, pygame.Rect(int(rect.left), int(rect.bottom), int(rect.right - rect.left),
                                                    int(rect.top - rect.bottom)))

    def draw_circle(screen, circ, color):
        pygame.draw.circle(screen, color, (int(circ.centre.x),
                                           int(circ.centre.y)), int(circ.radius))

    def draw_human(screen, human):
        # print("Shit!")
        r = human_radius
        p = human.circle.centre
        draw_circle(screen, human.circle, red)
        newp = MoveAlongAngle(p, human.rotation, 2 * human_radius)
        pygame.draw.line(screen, red, (p.x, p.y), (newp.x, newp.y), 4)
        myfont = pygame.font.Font(None, 20)
        textImage = myfont.render(str(human.hp), True, black)
        screen.blit(textImage, (human.circle.centre.x, human.circle.centre.y))


def RunGame(human_number):
    if DEBUG:
        pygame.init()
        screen = pygame.display.set_mode((width_of_screen, height_of_screen))
        pygame.display.set_caption("Door Kickers")

    log = {}

    walls, humans, ball = Init(human_number, log)
    logs.append(log)
    for i in range(human_number):
        log["number"] = i
        sendLog(log, 0, i)

    # return
    fireballs = []
    meteors = []

    log = {}
    log["humans"] = str(humans)
    log["fireballs"] = str(fireballs)
    log["meteors"] = str(meteors)
    log["balls"] = str(ball)
    eventlist = []

    for human in humans:
        eventlist.append(
            [8, human.number, human.circle.centre.x, human.circle.centre.y])
    log["events"] = str(eventlist)
    listener = Listen(human_number)
    listener.setDaemon(True)
    listener.start()
    sendLog(log)

    score = [0.0] * human_number
    death_time = [0]*human_number
    timecnt = 0
    while timecnt < time_of_game:
        if DEBUG:
            print("-----------------Time = {}-----------------".format(timecnt))
        eventlist = []
        timecnt += 1
        if DEBUG:
            screen.fill(white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

        if ball.belong != -1:
            score[ball.belong] += 1

        for i in range(human_number):
            if humans[i] == None:
                if death_time[i]==0:
                    x, y = StartPoints.sample(n=1).iloc[0]
                    c = Circle(Point(x, y), human_radius)
                    while CircleIntersection(c, ball.circle):
                        x, y = StartPoints.sample(n=1).iloc[0]
                        c = Circle(Point(x, y), human_radius)
                    rot = random.randint(0, 359)
                    humans[i] = Human(Point(x, y), rot, i)
                    eventlist.append([8, i, x, y])
                else:
                    death_time[i]-=1

        analysis = []
        #return_values = []

        time.sleep(1.0 / frames_per_second)
        for i in range(human_number):
            analysis.append(copy.deepcopy(listener.ans[i]))
            if DEBUG:
                print('Player {}:'.format(i), listener.ans[i])
            listener.ans[i] = (0, 0, 0)



        for a, human in zip(analysis, humans):
            if human != None:
                if a[0] == 1:
                    move(human, a[1], a[2], walls)
                elif a[0] == 2:
                    rotate(human, a[1])

        UpdateWeaponMap(walls, fireballs, meteors, 1, eventlist)

        for a, human in zip(analysis, humans):
            if human!=None:
                if a[0] == 3:
                    if shoot(human, fireballs, walls):
                        eventlist.append([1, human.number])
                elif a[0] == 4:
                    if throw(human, meteors, Point(a[1], a[2]), walls):
                        eventlist.append([4, human.number])

        delFireballs = []
        delMeteors = []

        for fireball in fireballs:
            Flag = True
            for human in humans:
                if human!=None:
                    if CircleIntersection(human.circle, fireball.circle):
                        delFireballs.append(fireball)
                        Flag = False
                        break
            if not Flag:
                eventlist.append(
                    [6, fireball.circle.centre.x, fireball.circle.centre.y])
                for human in humans:
                    if human!=None:
                        if CircleIntersection(human.circle, fireball.attack_range):
                            human.hp -= fireball.hurt
                            eventlist.append([2, human.number, fireball.hurt])




        for fireball in delFireballs:
            fireballs.remove(fireball)

        for meteor in meteors:
            if meteor.time == 0:
                # print('Bomb!')
                eventlist.append([7, meteor.pos.x, meteor.pos.y])
                delMeteors.append(meteor)
                for human in humans:
                    if human!=None:
                        if CircleIntersection(human.circle, meteor.attack_range):
                            human.hp -= meteor.hurt
                            eventlist.append([2, human.number, meteor.hurt])

        for meteor in delMeteors:
            meteors.remove(meteor)

        delHumanNumbers = []

        for human in humans:
            if human!=None:
                if human.hp <= 0:
                    if ball.belong == human.number:
                        ball.belong = -1
                    delHumanNumbers.append(human.number)
                    eventlist.append([3, human.number])
                    # print(human.number)
                else:
                    if human.attack_time > 0:
                        human.attack_time -= 1
        for i in delHumanNumbers:
            humans[i] = None
            death_time[i] = time_of_death


        update_ball(ball, humans, eventlist)

        log = {}
        log["humans"] = str(humans)
        log["fireballs"] = str(fireballs)
        log["meteors"] = str(meteors)
        log["balls"] = str(ball)
        log["events"] = str(eventlist)
        sendLog(log)

        if DEBUG:
            for event in eventlist:
                if event[0]==1:
                    print("Player {} shoots!".format(event[1]))
                elif event[0]==2:
                    print("Player {} gets {} hurt!".format(event[1],event[2]))
                elif event[0]==3:
                    print("Player {} died!".format(event[1]))
                elif event[0]==4:
                    print("Player {} cast Meteor!".format(event[1]))
                elif event[0]==5:
                    print("Player {} gets ball!".format(event[1]))
                elif event[0]==6:
                    print("A Fireball splashes at ({},{})!".format(event[1],event[2]))
                elif event[0]==7:
                    print("A Meteor impacts at ({},{})!".format(event[1],event[2]))
                elif event[0]==8:
                    print("Player {} reincarnate at ({},{})!".format(event[1],event[2],event[3]))
                elif event[0]==9:
                    print("A Fireball disappears at ({},{})!".format(event[1],event[2]))



        if PYGAME:
            for wall in walls:
                draw_rectangle(screen, wall.rectangle, black)
            for meteor in meteors:
                draw_circle(screen, meteor.attack_range, yellow)
            for human in humans:
                if human is not None:
                    draw_human(screen, human)
            for fireball in fireballs:
                draw_circle(screen, fireball.circle, green)

            draw_circle(screen, ball.circle, blue)
            pygame.display.flip()

    log = {}
    log["scores"] = score
    sendLog(log, 2, -1)

    if DEBUG:
        print("################### Result ###################")
        for i, sc in enumerate(score):
            print(i, ":", sc)
        print("###################        ###################")

    with open("log.json", "w")as file:
        json.dump(logs, file)
    time.sleep(3)


if __name__ == "__main__":
    RunGame(int(sys.argv[2]))
    # try:
    #    if sys.argv[1] == '--ai-num' and sys.argv[2]:
    #        RunGame(int(sys.argv[2]))
    #    else:
    #        print('Invalid format!')
    # except Exception as e:
    #    logging.error(e)

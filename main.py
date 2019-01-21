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


# Created by frh
# Modified by xtx


def draw_rectangle(screen, rect, color):
    pygame.draw.rect(screen, color, pygame.Rect(int(rect.left), int(rect.bottom), int(rect.right - rect.left),
                                                int(rect.top - rect.bottom)))


def draw_circle(screen, circ, color):
    pygame.draw.circle(screen, color, (int(circ.centre.x),
                                       int(circ.centre.y)), int(circ.radius))


def draw_human(screen, human):
    #print("Shit!")
    r = human_radius
    p = human.circle.centre
    draw_circle(screen, human.circle, red)
    newp = MoveAlongAngle(p, human.rotation, 2 * human_radius)
    pygame.draw.line(screen, red, (p.x, p.y), (newp.x, newp.y), 4)
    myfont = pygame.font.Font(None, 20)
    textImage = myfont.render(str(human.hp), True, black)
    screen.blit(textImage, (human.circle.centre.x, human.circle.centre.y))


def GenerateMap(Map, width, height):
    for i in range(width):
        for j in range(height):
            if random.random() < density_of_wall:
                Map[i][j] = True
            else:
                Map[i][j] = False

    Cnt2 = [0] * height
    Cnt = []
    for i in range(width):
        Cnt.append(copy.deepcopy(Cnt2))
    Cnt2 = copy.deepcopy(Cnt)

    def count1(i, j):
        ans = 0
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                if 0 <= x and x <= width - 1 and 0 <= y and y <= height - 1:
                    ans += int(Map[x][y])
                else:
                    ans += 1
        return ans

    def count2(i, j):
        ans = 0
        for x in range(i - 2, i + 3):
            for y in range(j - 2, j + 3):
                if max(abs(x - i), abs(y - j)) >= 2:
                    if 0 <= x and x <= width - 1 and 0 <= y and y <= height - 1:
                        ans += int(Map[x][y])
                    else:
                        ans += 1
        return ans

    for Round in range(4):
        for i in range(width):
            for j in range(height):
                Cnt[i][j] = count1(i, j)
        for i in range(width):
            for j in range(height):
                Cnt2[i][j] = count2(i, j)

        for i in range(width):
            for j in range(height):
                if Cnt[i][j] >= 5 or Cnt2[i][j] <= 2:
                    Map[i][j] = True
                else:
                    Map[i][j] = False

    for Round in range(3):
        for i in range(width):
            for j in range(height):
                Cnt[i][j] = count1(i, j)
        for i in range(width):
            for j in range(height):
                if Cnt[i][j] >= 5:
                    Map[i][j] = True
                else:
                    Map[i][j] = False


StartPoints = []


def bfs(stx,sty,Map,color,width,height):
    color[stx][sty] = True
    dxs = [-1,1,0,0]
    dys = [0,0,-1,1]

    queue = [(stx,sty)]

    while queue!=[]:
        x,y = queue.pop(0)
        for dx,dy in zip(dxs,dys):
            if 0<=x+dx and x+dx<width and 0<=y+dy and y+dy<height and (not Map[x+dx][y+dy]) and (not color[x+dx][y+dy]):
                color[x+dx][y+dy]=True
                queue.append((x+dx,y+dy))





def check(Map, width, height):

    color = []
    for i in range(width):
        color.append([False] * height)

    for i in range(width):
        for j in range(height):
            if (not Map[i][j]) and (not color[i][j]):
                bfs(i, j, Map,color,width,height)
                break
        else:
            continue
        break
    ans = 0
    for i in range(width):
        for j in range(height):
            if (not Map[i][j]) and (not color[i][j]):
                return False
            else:
                ans += int(Map[i][j])

    if ans> width*height*(density_of_wall+0.2):
        return False

    return True


def Init():
    walls = []

    global width, height

    width = int(width_of_screen / room_size)
    height = int(height_of_screen / room_size)

    global w_offset, h_offset

    w_offset = 1.0 * (width_of_screen - room_size * width) / 2
    h_offset = 1.0 * (height_of_screen - room_size * height) / 2

    Map = []
    for i in range(width):
        Map.append(copy.deepcopy([False] *height))

    GenerateMap(Map, width, height)

    while not check(Map, width, height):
        print("Failed")
        GenerateMap(Map, width, height)

    for i in range(width):
        for j in range(height):
            if(Map[i][j]):
                print("O", end='')
            else:
                print("*", end='')
        print()
    print()


    RealMap = []
    for i in range(width):
        RealMap.append([False]*height)


    ReachPoints = []

    def bfs(x,y):
        nonlocal ReachPoints
        ReachPoints = [(x,y)]
        queue = [(x,y)]
        color = []
        for i in range(width):
            color.append([False]*height)
        color[x][y]=True
        dxs = [-1,1,0,0]
        dys = [0,0,-1,1]
        while queue!=[]:
            x,y = queue.pop(0)
            for dx,dy in zip(dxs,dys):
                if 0<=x+dx and x+dx<width and 0<=y+dy and y+dy<height and (Map[x+dx][y+dy]) and (not color[x+dx][y+dy]):
                    color[x+dx][y+dy]=True
                    queue.append((x+dx,y+dy))
                    ReachPoints.append((x+dx,y+dy))


    rightest = []
    for i in range(width):
        rightest.append([0]*height)



    ans = 0
    for i in range(width):
        for j in range(height):
                ans += int(Map[i][j])

    for Round in range(max_num_of_wall):
        for j in range(height):
            for i in range(width-1,-1,-1):
                if not Map[i][j]:
                    continue
                if i==width-1:
                    rightest[i][j]=i
                else:
                    if Map[i+1][j]:
                        rightest[i][j]=rightest[i+1][j]
                    else:
                        rightest[i][j]=i
        ansx1,ansx2,ansy1,ansy2 = 0,-1,0,-1
        if ans == 0:
            break
        IsWall = []
        for x in range(width):
            for y in range(height):
                if Map[x][y]:
                    IsWall.append((x,y))
        assert(len(IsWall)==ans)
        index = random.randint(0,len(IsWall)-1)
        x,y = IsWall[index]
        # 选取该联通块，使用面积最大的矩形覆盖
        bfs(x,y)
        for x,y in ReachPoints:
            assert(Map[x][y]==True)
            # left bottom point
            right = width
            for yy in range(y,height):
                if not Map[x][yy]:
                    break
                right = min(right,rightest[x][yy])
                x1,x2,y1,y2 = x,right,y,yy
                if (x2-x1+1)*(y2-y1+1)>(ansx2-ansx1+1)*(ansy2-ansy1+1):
                    ansx1,ansx2,ansy1,ansy2 = x1,x2,y1,y2

        for i in range(ansx1,ansx2+1):
            for j in range(ansy1,ansy2+1):
                RealMap[i][j]=True
                Map[i][j]=False

        ans -= (ansx2-ansx1+1)*(ansy2-ansy1+1)
        ansx1 = w_offset + ansx1 * room_size
        ansx2 = w_offset + (ansx2+1) * room_size
        ansy1 = h_offset + ansy1 * room_size
        ansy2 = h_offset + (ansy2+1) * room_size

        walls.append(Wall(ansx1,ansx2,ansy1,ansy2))
    '''
    for i in range(width):
        for j in range(height):
            if(RealMap[i][j]):
                print("O", end='')
            else:
                print("*", end='')
        print()
    print()
    '''
    for x in range(width):
        for y in range(height):
            if not RealMap[x][y]:
                StartPoints.append((w_offset + (x + 0.5) * room_size,
                      h_offset + (y + 0.5) * room_size))


    for i in range(width):
        for j in range(height):
            if(RealMap[i][j]):
                print("O", end='')
            else:
                print("*", end='')
        print()
    print()
    def generate_pos():
        return StartPoints[random.randint(0,len(StartPoints)-1)]

    ball_x, ball_y = generate_pos()

    ball = Ball(Point(ball_x,ball_y))

    humans = []

    for i in range(human_number):
        x, y = generate_pos()
        while (x==ball_x) and (y==ball_y):
            x,y = generate_pos()
        rot = random.randint(0, 359)

        humans.append(Human(Point(x, y), rot, i))

    return walls, humans, ball



def update_ball(ball, humans):
    if ball.belong is not None:
        ball.circle.centre = ball.belong.circle.centre
    else:
        for human in humans:
            if (human is not None) and CircleIntersection(ball.circle, human.circle):
                ball.belong = human
                ball.circle.centre = human.circle.centre


def move(human, dis, walls):
    if dis < 0:
        dis = 0
    if dis > human_speed_max:
        dis = human_speed_max
    oldcentre = human.circle.centre
    human.circle.centre = MoveAlongAngle(oldcentre, human.rotation, dis)
    if not LegalPos(human.circle, walls):
        human.circle.centre = oldcentre


def shoot(human, fireballs, walls):
    if human.attack_time == 0:
        human.attack_time = human.fireball_interval
        p = MoveAlongAngle(human.circle.centre, human.rotation,
                           human_radius + fireball_radius)
        if LegalPos(Circle(p, fireball_radius), walls):
            fireballs.append(Fireball(p, human.rotation))


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


class Dispatcher(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.return_value = None
        self.func = func
        self.start()

    def run(self):
        self.return_value = self.func()


def func(ai):
    patcher = Dispatcher(ai.analysis)
    # print("infunc", time.time())
    patcher.join(timeout=time_of_round)
    # print("infunc", time.time())
    # time.sleep(time_of_round)

    if patcher.return_value:
        return patcher.return_value
    else:
        return (0, 0, 0)


def RunGame():
    pygame.init()
    screen = pygame.display.set_mode((width_of_screen, height_of_screen))
    pygame.display.set_caption("Door Kickers")
    #Init()

    walls, humans, ball = Init()
    #return
    fireballs = []
    meteors = []
    ais = []
    for i in range(human_number):
        ais.append(AI_player(i, copy.deepcopy(ball), copy.deepcopy(walls), copy.deepcopy(fireballs), copy.deepcopy(humans), copy.deepcopy(meteors)))
    #ais.append(Time_Out_AI_player(0, ball, walls, bullets, humans, grenades))
    # for i in range(human_number - 1):
    #    ais.append(AI_player(i, ball, walls, bullets, humans, grenades))

    score = [0.0] * human_number
    start_time = time.time()
    while time.time() - start_time < time_of_game:

        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if ball.belong != None:
            score[ball.belong.number] += 1

        def randomfloat(x):
            return random.randint(0, x - 1) + random.random()

        def generate_pos():
            return StartPoints[random.randint(0,len(StartPoints)-1)]

        for i in range(human_number):
            if humans[i] == None:
                x,y = generate_pos()
                c = Circle(Point(x, y), human_radius)
                while CircleIntersection(c, ball.circle):
                    x, y = generate_pos()
                    c = Circle(Point(x, y), human_radius)
                rot = random.randint(0, 359)
                humans[i] = Human(Point(x, y), rot, i)

        analysis = []
        return_values = []
        n = human_number
        #print(time.time())
        pool = Pool(processes=n)

        for i in range(n):
            ais[i].refresh(ball, walls, fireballs, humans, meteors)
            return_values.append(pool.apply_async(func, args=(ais[i],)))
        pool.close()
        #print(time.time())
        pool.join()
        #print(time.time())
        #print()
        for i in return_values:
            analysis.append(i.get())

        for a, human in zip(analysis, humans):
            if a[0] == 1:
                move(human, a[1], walls)
            elif a[0] == 2:
                rotate(human, a[1])

        UpdateWeaponMap(walls, fireballs, meteors, 1)

        for a, human in zip(analysis, humans):
            if a[0] == 3:
                shoot(human, fireballs, walls)
            elif a[0] == 4:
                throw(human, meteors, Point(a[1], a[2]), walls)

        delFireballs = []
        delMeteors = []

        for fireball in fireballs:
            Flag = True
            for human in humans:
                if CircleIntersection(human.circle, fireball.circle):
                    delFireballs.append(fireball)
                    Flag = False
                    break
            if not Flag:
                for human in humans:
                    if CircleIntersection(human.circle, fireball.attack_range):
                        human.hp -= fireball.hurt

        for fireball in delFireballs:
            fireballs.remove(fireball)

        for meteor in meteors:
            if meteor.time == 0:
                #print('Bomb!')
                delMeteors.append(meteor)
                for human in humans:
                    if CircleIntersection(human.circle, meteor.attack_range):
                        human.hp -= meteor.hurt

        for meteor in delMeteors:
            meteors.remove(meteor)

        delHumanNumbers = []

        for human in humans:
            if human.hp <= 0:
                if ball.belong is human:
                    ball.belong = None
                delHumanNumbers.append(human.number)
                #print(human.number)
            else:
                if human.attack_time > 0:
                    human.attack_time -= 1
        for i in delHumanNumbers:
            humans[i]=None

        update_ball(ball, humans)

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
    for i, sc in enumerate(score):
        print(i, ":", sc)



if __name__ == "__main__":
    RunGame()

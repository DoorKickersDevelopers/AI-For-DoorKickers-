import pygame
from pygame import Rect
import sys
import random
import copy
import time
from AI_Player import AI_player
from Arguments import *
from BaseClass import *
from MySTL import *

# Created by frh
# Modified by xtx


def draw_rectangle(screen, rect, color):
    pygame.draw.rect(screen, color, pygame.Rect(int(rect.left), int(rect.bottom), int(rect.right - rect.left),
                                                int(rect.top - rect.bottom)))


def draw_circle(screen, circ, color):
    pygame.draw.circle(screen, color, (int(circ.centre.x),
                                       int(circ.centre.y)), int(circ.radius))


def draw_human(screen, human):
    r = human_radius
    p = human.circle.centre
    draw_circle(screen, human.circle, red)
    newp = MoveAlongAngle(p, human.rotation, 2 * human_radius)
    pygame.draw.line(screen, red, (p.x, p.y), (newp.x, newp.y), 4)
    myfont = pygame.font.Font(None, 20)
    textImage = myfont.render(str(human.hp), True, black)
    screen.blit(textImage, (human.circle.centre.x, human.circle.centre.y))


def dfs(lx, rx, ly, ry, Map):
    if rx - lx < min_space * 2 and ry - ly < min_space * 2:
        return
    op = random.randint(0, 1)
    if rx - lx < min_space * 2:
        op = 1
    if ry - ly < min_space * 2:
        op = 0
    if op == 0:
        posx = random.randint(lx + min_space, rx - min_space)
        posy = random.randint(ly, ry)
        for i in range(ly, ry + 1):
            if i != posy:
                if random.random() <= density_of_wall:
                    Map[posx][i] = True

        dfs(lx, posx - 1, ly, ry, Map)
        dfs(posx + 1, rx, ly, ry, Map)

    else:
        posx = random.randint(lx, rx)
        posy = random.randint(ly + min_space, ry - min_space)
        for i in range(lx, rx + 1):
            if i != posx:
                if random.random() <= density_of_wall:
                    Map[i][posy] = True
        # print(Map)
        dfs(lx, rx, ly, posy - 1, Map)
        dfs(lx, rx, posy + 1, ry, Map)


StartPoint = []


def Init():
    walls = []

    global width, height

    width = int(width_of_screen / room_size)
    height = int(height_of_screen / room_size)

    global w_offset, h_offset

    w_offset = 1.0 * (width_of_screen - room_size * width) / 2
    h_offset = 1.0 * (height_of_screen - room_size * height) / 2

    Map2 = [False] * height
    Map = []
    for i in range(width):
        Map.append(copy.deepcopy(Map2))

    dfs(0, width - 1, 0, height - 1, Map)

    NeedBuild = copy.deepcopy(Map)

    for x in range(width):
        for y in range(height):
            if NeedBuild[x][y]:
                xx = x
                for i in range(x, width):
                    if Map[i][y]:
                        xx = i
                    else:
                        break
                yy = y
                for j in range(y, width):
                    for i in range(x, xx + 1):
                        if not Map[i][j]:
                            break
                    else:
                        break
                    yy = j
                for i in range(x, xx + 1):
                    for j in range(y, yy + 1):
                        NeedBuild[i][j] = False
                walls.append(Wall(w_offset + x * room_size, w_offset + (xx + 1) *
                                  room_size, h_offset + y * room_size, h_offset + (yy + 1) * room_size))

    for x in range(width):
        for y in range(height):
            if not Map[x][y]:
                StartPoint.append((x, y))

    def generate_pos():
        return random.randint(0, width - 1), random.randint(0, height - 1)

    ball_x, ball_y = generate_pos()
    while Map[ball_x][ball_y]:
        ball_x, ball_y = generate_pos()

    ball = Ball(Point(w_offset + (ball_x + 0.5) * room_size,
                      h_offset + (ball_y + 0.5) * room_size))

    Map[ball_x][ball_y] = True

    humans = []

    for i in range(human_number):
        x, y = generate_pos()
        while Map[x][y]:
            x, y = generate_pos()
        x = w_offset + (x + 0.5) * room_size
        y = h_offset + (y + 0.5) * room_size

        rot = random.randint(0, 359)

        humans.append(Human(Point(x, y), rot, i))

    return walls, humans, ball


def update_ball(ball, humans):
    if ball.belong is not None:
        ball.circle.centre = ball.belong.circle.centre
    else:
        for human in humans:
            if CircleIntersection(ball.circle, human.circle):
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


def shoot(human, bullets, walls):
    if human.fire_time == 0:
        human.fire_time = human_fire_interval
        p = MoveAlongAngle(human.circle.centre, human.rotation,
                           human_radius + bullet_radius)
        if LegalPos(Circle(p, bullet_radius), walls):
            bullets.append(Bullet(p, human.rotation))


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


def throw(human, grenades, walls):
    if human.grenade_number > 0:
        human.grenade_number -= 1
        p = MoveAlongAngle(human.circle.centre, human.rotation,
                           human_radius + grenade_radius)
        if LegalPos(Circle(p, grenade_radius), walls):
            grenades.append(Grenade(p, human.rotation))


def RunGame():
    pygame.init()
    screen = pygame.display.set_mode((width_of_screen, height_of_screen))
    pygame.display.set_caption("Door Kickers")
    walls, humans, ball = Init()
    bullets = []
    grenades = []
    ais = []
    for i in range(human_number):
        ais.append(AI_player(i, ball, walls, bullets, humans, grenades))
    score = [0.0] * human_number
    start_time = time.time()
    while time.time() - start_time < time_of_game:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if ball.belong != None:
            score[ball.belong.number] += 1

        analysis = []
        for i in range(len(ais)):
            ais[i].refresh(i, ball, walls, bullets, humans, grenades)
            # analysis.append(ais[i].analysis())
            analysis.append((4, 0, human_speed_max))

        for a, human in zip(analysis, humans):
            if a[0] == 1:
                rotate(human, a[1])
            elif a[0] == 2:
                move(human, a[2], walls)

        bullets, grenades = FutureWeaponMap(walls, bullets, grenades, 1)
        if ball.belong != None:
            ball.circle.centre = ball.belong.circle.centre

        for a, human in zip(analysis, humans):
            if a[0] == 3:
                shoot(human, bullets, walls)
            elif a[0] == 4:
                throw(human, grenades, walls)

        newbullets = []
        newgrenades = []

        for bullet in bullets:
            Flag = True
            for human in humans:
                if CircleIntersection(human.circle, bullet.circle):
                    human.hp -= bullet_hurt
                    Flag = False
            if Flag:
                newbullets.append(bullet)

        for grenade in grenades:
            if grenade.time <= 0:
                for human in humans:
                    if CircleIntersection(human.circle, Circle(grenade.circle.centre, explode_radius)):
                        human.hp -= explode_hurt
            else:
                newgrenades.append(grenade)

        grenades = newgrenades
        bullets = newbullets

        newhumans = []

        def generate_pos():
            t = random.randint(0, len(StartPoint) - 1)
            x, y = StartPoint[t]
            x = w_offset + (x + 0.5) * room_size
            y = h_offset + (y + 0.5) * room_size
            return x, y

        for human in humans:
            if human.hp <= 0:
                if ball.belong is human:
                    ball.belong = None
                while True:
                    x, y = generate_pos()
                    Flag = True
                    for bullet in bullets:
                        if CircleIntersection(Circle(Point(x, y), human_radius), bullet.circle):
                            Flag = False
                    if Flag:
                        newhumans.append(
                            Human(Point(x, y), random.randint(0, 359), human.number))
                        break
            else:
                if human.fire_time > 0:
                    human.fire_time -= 1
                newhumans.append(human)

        humans = newhumans

        for wall in walls:
            draw_rectangle(screen, wall.rectangle, black)
        for human in humans:
            draw_human(screen, human)
        for bullet in bullets:
            draw_circle(screen, bullet.circle, green)
        for grenade in grenades:
            draw_circle(screen, grenade.circle, yellow)

        draw_circle(screen, ball.circle, blue)
        pygame.display.flip()

    for i, sc in enumerate(score):
        print(i, ":", sc)


RunGame()

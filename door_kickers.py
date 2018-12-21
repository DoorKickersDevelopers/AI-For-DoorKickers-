import pygame
from pygame import Rect
import sys
import random
import AI
from AI_Player import AI_player
from Arguments import *
from BaseClass import *
from MySTL import *


#new
#new
def draw_rectangle(screen, rect, color):
    pygame.draw.rect(screen, color, pygame.Rect(int(rect.left), int(rect.bottom), int(rect.right - rect.left),
                                              int(rect.top - rect.bottom)))


def draw_circle(screen, circ, color):
    pygame.draw.circle(screen, color, (int(circ.centre.x), int(circ.centre.y)), int(circ.radius))


def draw_human(screen, human):
    r = human_radius
    p = human.circle.centre
    draw_circle(screen, human.circle, red)
    newp = MoveAlongAngle(p, human.rotation, 2*human_radius)
    pygame.draw.line(screen, red, p.tolist(), newp.tolist(), 4)
    myfont = pygame.font.Font(None, 20)
    textImage = myfont.render(str(human.hp), True, black)
    screen.blit(textImage, human.circle.centre.tolist())


def InitWalls(num):
    walls = []
    width = width_of_wall
    for i in range(num):
        left = random.randint(0, height_of_screen - 2 * width)
        length = random.randint(2 * width, height_of_screen - left)
        top = random.randint(0, height_of_screen)
        if i % 2 == 0:
            walls.append(Wall(left, left+width, top, top+length))
        else:
            walls.append(Wall(top, top+length, left, left+width))
    return walls


def InitHumans(num, walls):
    humans = []
    for i in range(num):
        while True:
            x = random.randint(0, width_of_screen)
            y = random.randint(0, height_of_screen)
            posi = Point(x, y)
            if LegalPos(Circle(posi, human_radius), walls):
                humans.append(Human(posi, random.randint(0, 359), i))
                break
    return humans


def InitBall(walls):
    while True:
        x = random.randint(0, width_of_screen)
        y = random.randint(0, height_of_screen)
        p = Point(x, y)
        if LegalPos(Circle(p, ball_radius), walls):
            return Ball(p)


def update_ball(ball, humans):
    if ball.belong is not None:
        ball.circle.centre = ball.belong.circle.centre
    else:
        for human in humans:
            if CircleIntersection(ball.circle, human.circle):
                ball.belong = human
                ball.circle.centre = human.circle.centre


def human_move(self, dis, walls):
    if dis < 0:
        dis = 0
    if dis > human_speed_max:
        dis = human_speed_max
    oldcentre = self.circle.centre
    self.circle.centre = MoveAlongAngle(oldcentre, self.rotation, dis)
    if not LegalPos(self.circle, walls):
        self.circle.centre = oldcentre


def human_shoot(self):
    if self.fire_time == 0:
        self.fire_time = human_fire_interval
        p = MoveAlongAngle(self.circle.centre, self.rotation, human_radius+bullet_radius)
        return Bullet(p, self.rotation)
    return None


def human_throwGrenade(self):
    if self.grenade_number > 0:
        self.grenade_number -= 1
        p = MoveAlongAngle(self.circle.centre, self.rotation, human_radius+grenade_radius)
        return Grenade(p, self.rotation)
    return None


def RunGame():
    pygame.init()
    screen = pygame.display.set_mode((width_of_screen, height_of_screen))
    pygame.display.set_caption("Door Kickers")
    walls = InitWalls(number_of_walls)
    humans = InitHumans(human_number, walls)
    ball = InitBall(walls)
    time = 0
    bullets = []
    grenades = []
    ais = []
    for i in range(human_number):
        ais.append(AI.MyAI(i, ball, walls, bullets, humans, grenades,screen))
    #this is frh's test code
    '''
    test = False
    humans[0].circle.centre = Point(100, 100)
    humans[0].rotation = 0
    humans[1].circle.centre = Point(200, 100)
    humans[1].rotation = 180
    ball.circle.centre = Point(230, 130)
    '''
    while True:
        screen.fill(white)
        time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if time == 20:
            time = 0
            # ai决策

            analysis = []
            for i in range(len(ais)):
                ais[i].getdata(i, ball, walls, bullets, humans, grenades)
                analysis.append(ais[i].analysis())
            # 逻辑部分，人的移动
            for i in range(len(ais)):
                ana = analysis[i]
                type = ana[0]
                if type == 1:
                    humans[i].rotate(ana[1])
                elif type == 2:
                    human_move(humans[i],ana[2], walls)
                elif type == 3:
                    b = human_shoot(humans[i])
                    if b is not None:
                        bullets.append(b)
                else:
                    g = human_throwGrenade(humans[i])
                    if g is not None:
                        grenades.append(g)

            #this is frh's test code
            '''
            if True:
                # test
                if test is True:
                    human_move(humans[0], human_speed_max, walls)
                b = human_shoot(humans[0])
                if b is not None:
                    bullets.append(b)
                g = human_throwGrenade(humans[1])
                if g is not None:
                    grenades.append(g)
                human_move(humans[1], human_speed_max, walls)
                humans[1].rotate(0-human_rotate_max)
            '''


        # 子弹、炸弹的移动
        explode_to_paint = []
        bullets_to_delete = []
        bullets, newgrenades = FutureWeaponMap(walls, bullets, grenades, 1)
        #如果子弹撞墙或撞人则消失
        for bullet in bullets:
            for human in humans:
                if CircleIntersection(human.circle, bullet.circle):
                    human.hp -= bullet_hurt
                    bullets_to_delete.append(bullet)
        for i in bullets_to_delete:
            bullets.remove(i)
        for grenade in grenades:
            if grenade.explode():
                explode_to_paint.append(Circle(grenade.circle.centre, explode_radius))
        for explode in explode_to_paint:
            for human in humans:
                if CircleIntersection(explode, human.circle):
                    human.hp -= explode_hurt
        grenades = newgrenades

        # 人的更新
        for human in humans:
            if human.update() is False:
                if ball.belong is human:
                    ball.belong = None
                index = humans.index(human)
                humans[index] = InitHumans(1, walls)[0]
        update_ball(ball, humans)

        
        for wall in walls:
            draw_rectangle(screen, wall.rectangle, black)
        for human in humans:
            draw_human(screen, human)
        for bullet in bullets:
            draw_circle(screen, bullet.circle, green)
        for grenade in grenades:
            draw_circle(screen, grenade.circle, yellow)
        for explode in explode_to_paint:
            pygame.draw.circle(screen, yellow, explode.centre.tolist(), explode_radius)
        draw_circle(screen, ball.circle, blue)
        pygame.display.flip()
        

RunGame()
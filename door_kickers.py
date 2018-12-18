import pygame
from pygame import Rect
import sys
import random
import math
import AI
from AI_Player import AI_player


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

number_of_walls = 10
width_of_walls = 30

height_of_screen = 600
width_of_screen = 800

human_numbers = 3
human_hp = 100
human_grenade_number = 3
human_fire_interval = 250
human_r = 10
human_speed_max = 4
human_rotate_max = 10

velocity_of_bullets = 1  # v*5
bullets_r = 5
bullets_hurt = 10

grenades_r = 5
grenades_time = 200
velocity_of_grenades = 1  # v*5
explode_r = [10, 20, 30, 40, 50]
explode_hurt = [50, 40, 30, 20, 10]

ball_r = 8

walls = []
humans = []
bullets = []
grenades = []
ais = []

class dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, offset):
        self.x += offset.x
        self.y += offset.y

    def copy(self):
        return dot(self.x, self.y)

    def tolist(self):
        return [int(self.x), int(self.y)]

    def distance_square(self, o):
        return (self.x - o.x) * (self.x - o.x) + (self.y - o.y) * (self.y - o.y)


def offset_of_rotation(l, r):
    return dot(l * math.cos(r*2*math.pi/360), l * math.sin(r*2*math.pi/360))


def position_valid(position, radius):
    if not (0 <= position.x <= width_of_screen and 0 <= position.y <= height_of_screen):
        print("crashintothescreen")
        return False
    for wall in walls:
        x = int(position.x)
        y = int(position.y)
        l = wall.left
        r = wall.right
        t = wall.top
        d = wall.bottom
        if (l-radius <= x <= r+radius) and (t-radius <= y <= d+radius):
            print("crashintothewall")
            return False
    return True





class Ball:
    def __init__(self, p):
        self.position = p
        self.belong = -1

    def human_crash(self):
        for human in humans:
            if self.position.distance_square(human.position) <= (human_r + ball_r) * (human_r + ball_r):
                self.belong = human.node
                self.position = human.position
                return True
        return False

    def update(self):
        if self.belong >= 0:
            self.position = humans[self.belong].position
        else:
            self.human_crash()


class Bullets:
    def __init__(self, p, v):
        self.position = p
        self.velocity = v

    def crash_into_human(self, newp):
        for human in humans:
            dis = newp.distance_square(human.position)
            mindis = (human_r + bullets_r)*(human_r + bullets_r)
            if dis < mindis:
                human.hp -= bullets_hurt
                print("crashintopeople")
                return True
        return False

    def move(self):
        newp = self.position.copy()
        newp.add(self.velocity)
        if position_valid(newp, bullets_r):
            if self.crash_into_human(newp) is False:
                self.position = newp
                return True
        return False


class Grenades:
    def __init__(self, p, v):
        self.position = p
        self.velocity = v
        self.time = grenades_time

    def adjust(self):
        x = self.position.x
        y = self.position.y
        vx = self.velocity.x
        vy = self.velocity.y
        ra = grenades_r
        if x < ra or x > width_of_screen - ra:
            self.velocity.x = -vx
            print("fantan")
        if y < ra or y > height_of_screen - ra:
            self.velocity.y = -vy
            print('fantan')
        for wall in walls:
            l = wall.left
            r = wall.right
            t = wall.top
            d = wall.bottom
            if l <= x <= r and t - ra <= y <= d + ra:
                self.velocity.y = -vy
            if t <= y <= d and l - ra <= x <= r + ra:
                self.velocity.x = -vx

    def explode(self):
        self.time -= 1
        if self.time == 0:
            for human in humans:
                distance = math.sqrt(self.position.distance_square(human.position))
                for i in range(5):
                    if distance < explode_r[i]:
                        human.hp -= explode_hurt[i]
                        break
            return True
        return False

    def move(self):
        newp = self.position.copy()
        newp.add(self.velocity)
        self.position = newp
        self.adjust()


class Humans:
    def __init__(self, p, r, n):
        self.position = p
        self.rotation = r
        self.hp = human_hp
        self.grenade_number = human_grenade_number
        self.fire_time = 0
        self.node = n

    def move(self, length):
        offset = offset_of_rotation(length, self.rotation)
        offset.add(self.position)
        if position_valid(offset, human_r):
            self.position = offset

    def rotate(self, r):
        self.rotation += r
        if self.rotation > 360:
            self.rotation -= 360
        if self.rotation < 0:
            self.rotation += 360

    def shoot(self):
        if self.fire_time == 0:
            self.fire_time = human_fire_interval
            offset = offset_of_rotation(2*human_r, self.rotation)
            offset.add(self.position)
            bullets.append(Bullets(offset, offset_of_rotation(velocity_of_bullets, self.rotation)))
            return True
        return False

    def grenade(self):
        if self.grenade_number > 0:
            self.grenade_number -= 1
            grenades.append(Grenades(self.position, offset_of_rotation(velocity_of_grenades, self.rotation)))
            return True
        return False

    def update(self):
        if self.fire_time > 0:
            self.fire_time -= 1
        if self.hp <= 0:
            return False
        return True


def draw_human(screen, human):
    r = human_r
    pygame.draw.circle(screen, red, human.position.tolist(), r)
    p = human.position
    offset = offset_of_rotation(2 * r, human.rotation)
    offset.add(p)
    pygame.draw.line(screen, red, p.tolist(), offset.tolist(), 4)
    myfont = pygame.font.Font(None, 20)
    textImage = myfont.render(str(human.hp), True, black)
    screen.blit(textImage, human.position.tolist())


def build_human(i):
    p = dot(0, 0)
    while True:
        p.x = random.randint(0, width_of_screen)
        p.y = random.randint(0, height_of_screen)
        if position_valid(p, human_r):
            break
    rotation = random.randint(0, 359)
    return Humans(p, rotation, i)


def build_wall(i):
    width = width_of_walls
    left = random.randint(0, height_of_screen - 2 * width)
    length = random.randint(2 * width, height_of_screen - left)
    top = random.randint(0, height_of_screen)
    if i % 2 == 0:
        return Rect(left, top, length, width)
    else:
        return Rect(top, left, width, length)


def build_ball():
    p = dot(0, 0)
    while True:
        p.x = random.randint(0, width_of_screen)
        p.y = random.randint(0, height_of_screen)
        if position_valid(p, ball_r):
            break
    return Ball(p)


def Run_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Door Kickers")
    for i in range(number_of_walls):
        walls.append(build_wall(i))
    for i in range(human_numbers):
        humans.append(build_human(i))
    ball = build_ball()
    time = 0
    explode_to_paint = []
    for i in range(human_numbers):
        ais.append(AI.MyAI(i, ball, walls, bullets, humans, grenades,screen))

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
                    if ana[1] > human_rotate_max:
                        ana[1] = human_rotate_max
                    elif ana[1] < -human_rotate_max:
                        ana[1] = -human_rotate_max
                    humans[i].rotate(ana[1])
                elif type == 2:
                    if ana[2] > human_speed_max:
                        ana[2] = human_speed_max
                    elif ana[2] < -human_speed_max:
                        ana[2] = -human_speed_max
                    humans[i].move(ana[2])
                elif type == 3:
                    humans[i].shoot()
                else:
                    humans[i].grenade()

        # 子弹、炸弹的移动
        if time % 4 == 0:
            explode_to_paint = []
            bullets_to_delete = []
            grenade_to_delete = []
            for bullet in bullets:
                if bullet.move() is False:
                    bullets_to_delete.append(bullet)
            for i in bullets_to_delete:
                bullets.remove(i)
            for grenade in grenades:
                grenade.move()
                if grenade.explode():
                    grenade_to_delete.append(grenade)
            for grenade in grenade_to_delete:
                explode_to_paint.append(grenade)
                grenades.remove(grenade)

        # 人的更新
            for human in humans:
                if human.update() is False:
                    test = True
                    index = humans.index(human)
                    humans[index] = build_human(index)
                    if index == ball.belong:
                        ball.belong = -1

        ball.update()

        
        for wall in walls:
            pygame.draw.rect(screen, black, wall)
        for human in humans:
            draw_human(screen, human)
        for bullet in bullets:
            pygame.draw.circle(screen, green, bullet.position.tolist(), bullets_r)
        for grenade in grenades:
            pygame.draw.circle(screen, yellow, grenade.position.tolist(), grenades_r)
        for explode in explode_to_paint:
            pygame.draw.circle(screen, yellow, explode.position.tolist(), explode_r[-1])
        pygame.draw.circle(screen, blue, ball.position.tolist(), ball_r)
        pygame.display.flip()
        

Run_game()




def test():
    # init
    humans[0].position = dot(300, 300)
    humans[1].position = dot(300, 400)
    humans[0].rotation = 90
    humans[1].rotation = 0
    ball.position = dot(320, 420)
    #while
    humans[0].shoot()
    humans[1].move(4)
    humans[1].rotate(10)
    humans[1].grenade()
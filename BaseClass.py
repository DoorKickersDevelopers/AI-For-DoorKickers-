import math
from math import sqrt, fabs, atan2
from Arguments import *
import copy


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)

    def __mul__(self, p):
        return self.x * p.y - self.y * p.x


class Line(object):
    def __init__(self, p1, p2):
        if p1.x == p2.x and p1.y == p2.y:
            raise Exception("create an instance of line with illegal argument")
        self.p1 = copy.deepcopy(p1)
        self.p2 = copy.deepcopy(p2)

    def Points(self):
        return self.p1, self.p2


class Rectangle(object):
    def __init__(self, left, right, bottom, top):
        if right <= left or top <= bottom:
            raise Exception(
                "create an instance of Rectangle with illegal argument")
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

    def Points(self):
        return Point(self.left, self.bottom), Point(self.left, self.top), Point(self.right, self.bottom), Point(self.right, self.top)

    def expand(e):
        return Rectangle(self.left + e, self.right - e, self.bottom + e, self.top - e)


class TargetArea:
    radius = target_radius

    def __init__(self, pos):
        self.pos = copy.deepcopy(pos)


class Ball:
    radius = ball_radius

    def __init__(self, birth_pos, faction):
        self.birth_pos = copy.deepcopy(birth_pos)
        self.faction = faction

    def reset(self):
        self.pos = copy.deepcopy(self.birth_pos)
        self.belong = -1

    def __repr__(self):
        return "[{},{},{},{}]".format(self.pos.x, self.pos.y, self.belong, self.faction)


class Fireball:
    radius = fireball_radius
    velocity = fireball_velocity
    hurt = splash_hurt
    attack_radius = splash_radius

    def __init__(self, pos, rot, from_number):
        self.pos = copy.deepcopy(pos)
        self.rot = rot
        self.from_number = from_number

    def __repr__(self):
        return "[{},{},{},{}]".format(self.pos.x, self.pos.y, self.rot, self.from_number)


class Meteor:
    hurt = explode_hurt
    attack_radius = explode_radius

    def __init__(self, pos, from_number):
        self.time = meteor_delay
        self.pos = pos
        self.from_number = from_number

    def __repr__(self):
        return "[{},{},{},{}]".format(self.pos.x, self.pos.y, self.time, self.from_number)


class Human:
    velocity = human_velocity
    fireball_interval = human_fireball_interval
    meteor_interval = human_meteor_interval
    flash_interval = human_flash_interval
    meteor_cast_distance = meteor_distance
    flash_cast_distance = flash_distance

    def __init__(self, number, pos):
        self.birth_pos = copy.deepcopy(pos)
        self.number = number
        self.death_time = 0
        self.faction = number % faction_number

    def reset(self):
        self.hp = human_hp
        self.meteor_number = human_meteor_number
        self.flash_number = human_flash_number
        self.meteor_time = 0
        self.flash_time = 0
        self.inv_time = frames_of_invincible
        self.pos = copy.deepcopy(self.birth_pos)
        self.fireball_time = 0

    def __repr__(self):
        return "[{},{},{},{},{},{},{},{},{},{},{}]".format(
            self.number, self.pos.x, self.pos.y, self.hp, self.meteor_number, self.meteor_time, self.flash_number, self.flash_time, self.fireball_time, self.death_time, self.inv_time)


class Wall(Rectangle):
    def __init__(self, left, right, bottom, top):
        super(Wall, self).__init__(left, right, bottom, top)

    def __repr__(self):
        return "[{},{},{},{}]".format(self.left, self.right, self.bottom, self.top)

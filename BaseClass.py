import math
from math import sqrt, fabs, atan2
from Arguments import *


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point({},{})".format(self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return self.x * other.y - self.y * other.x


class Line(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        if p1.x == p2.x and p1.y == p2.y:
            raise Exception("create an instance of line with illegal argument")

    def Points(self):
        return self.p1, self.p2

    def __repr__(self):
        return "Line( {} , {} )".format(self.p1.__repr__(), self.p2.__repr__())


class Rectangle(object):
    def __init__(self, left, right, bottom, top):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        if self.right <= self.left or self.top <= self.bottom:
            raise Exception(
                "create an instance of Rectangle with illegal argument")

    def __repr__(self):
        return "Rect(x:[{},{}],y:[{},{}])".format(self.left, self.right, self.bottom, self.top)

    def Points(self):
        return Point(self.left, self.bottom), Point(self.left, self.top), Point(self.right, self.bottom), Point(self.right, self.top)

    def Lines(self):
        p1, p2, p3, p4 = self.Points()
        return Line(p1, p2), Line(p1, p3), Line(p2, p4), Line(p3, p4)

    def expand(self, d):
        return Rectangle(self.left - d, self.right + d, self.bottom - d, self.top + d)


class Circle(object):
    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius
        if self.radius <= 0:
            raise Exception("create an instance of Circle with illegal radius")

    def __repr__(self):
        return "Circle(o:{},r:{})".format(self.centre, self.radius)


class Ball:
    def __init__(self, position):
        self.circle = Circle(position, ball_radius)
        self.belong = None

    def __repr__(self):
        if self.belong is None:
            num = -1
        else:
            num = self.belong.number
        return "[[{},{}],{}]".format(self.circle.centre.x, self.circle.centre.y, num)


class Fireball:
    velocity = velocity_of_fireball
    hurt = fireball_hurt

    def __init__(self, position, rotation):
        self.circle = Circle(position, fireball_radius)
        self.rotation = rotation
        self.attack_range = Circle(position, splash_radius)

    def __repr__(self):
        return "[[{},{}],{}]".format(self.circle.centre.x, self.circle.centre.y, self.rotation)


class Meteor:
    hurt = explode_hurt

    def __init__(self, position, last_time=meteor_delay):
        self.time = meteor_delay
        self.pos = position
        self.attack_range = Circle(position, explode_radius)

    def __repr__(self):
        return "[[{},{}],{}]".format(self.pos.x, self.pos.y, self.time)


class Human:
    velocity_max = human_speed_max
    rotation_max = human_rotate_max
    fireball_interval = human_fireball_interval
    meteor_interval = human_meteor_interval
    meteor_cast_distance = cast_distance

    def __init__(self, position, rotation, number):
        self.circle = Circle(position, human_radius)
        self.rotation = rotation
        self.hp = human_hp
        self.meteor_number = human_meteor_number
        self.attack_time = 0
        self.number = number

    def __repr__(self):
        return "[{},[{},{}],{},{},{},{}]".format(self.number, self.circle.centre.x, self.circle.centre.y, self.rotation, self.hp, self.meteor_number, self.attack_time)


class Wall:
    def __init__(self, left, right, bottom, top):
        self.rectangle = Rectangle(left, right, bottom, top)

    def __repr__(self):
        return "[{},{},{},{}]".format(self.rectangle.left, self.rectangle.right, self.rectangle.bottom, self.rectangle.top)

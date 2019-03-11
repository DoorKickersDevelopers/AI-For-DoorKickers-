import math
from math import sqrt, fabs, atan2
from BaseClass import *

eps = 1e-5


def L2Distance(p1, p2):
    return sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y))


def PointOnLine(p, l):
    if l.p1.x == l.p2.x:
        if p.x != l.p1.x:
            return False
        else:
            if min(l.p1.y, l.p2.y) <= p.y and p.y <= max(l.p1.y, l.p2.y):
                return True
            else:
                return False

    if fabs((l.p1.x - p.x) * (l.p2.y - p.y) - (l.p2.x - p.x) * (l.p1.y - p.y)) < eps:
        if min(l.p1.x, l.p2.x) <= p.x and p.x <= max(l.p1.x, l.p2.x):
            return True
        else:
            return False
    else:
        return False


def PointInRectangle(p, rect):
    return rect.left <= p.x and p.x <= rect.right and rect.bottom <= p.y and p.y <= rect.top


def RectangleIntersection(rect1, rect2):
    p1, p2, p3, p4 = rect1.Points()
    if PointInRectangle(p1, rect2) or PointInRectangle(p2, rect2)or PointInRectangle(p3, rect2)or PointInRectangle(p4, rect2):
        return True
    p1, p2, p3, p4 = rect2.Points()
    if PointInRectangle(p1, rect1) or PointInRectangle(p2, rect1)or PointInRectangle(p3, rect1)or PointInRectangle(p4, rect1):
        return True
    return False


def LineIntersection(l1, l2):
    def Rect(line):
        return Rectangle(min(line.p1.x, line.p2.x), max(line.p1.x, line.p2.x), min(line.p1.y, line.p2.y), max(line.p1.y, line.p2.y))

    if not RectangleIntersection(Rect(l1), Rect(l2)):
        return False

    if PointOnLine(l1.p1, l2) or PointOnLine(l1.p2, l2) or PointOnLine(l2.p1, l1) or PointOnLine(l2.p2, l1):
        return True

    p1 = l1.p2 - l1.p1
    if ((l2.p1 - l1.p1) * p1) * ((l2.p2 - l1.p1) * p1) >= 0:
        return False

    p2 = l2.p2 - l2.p1
    if ((l1.p1 - l2.p1) * p2) * ((l1.p2 - l2.p1) * p2) >= 0:
        return False

    return True


def Angle(p1, p2):
    if p1 == p2:
        raise Exception("Try to get Angle with illegal Argument")
    p = p2 - p1
    angle = atan2(p.y, p.x)
    return angle


def LineIntersectRect(l, rect):
    if PointInRectangle(l.p1, rect) or PointInRectangle(l.p2, rect):
        return True
    p1, p2, p3, p4 = rect.expand(eps).Points()

    return LineIntersection(l, Line(p1, p4)) or LineIntersection(l, Line(p2, p3))


def DisLinePoint(l, p):

    dot = (l.p2.x - l.p1.x) * (p.x - l.p1.x) + \
        (l.p2.y - l.p1.y) * (p.y - l.p1.y)
    d2 = (l.p2.x - l.p1.x) * (l.p2.x - l.p1.x) + \
        (l.p2.y - l.p1.y) * (l.p2.y - l.p1.y)
    if dot <= 0:
        return L2Distance(p, l.p1)
    if dot >= d2:
        return L2Distance(p, l.p2)

    r = dot / d2
    px = l.p1.x + (l.p2.x - l.p1.x) * r
    py = l.p1.y + (l.p2.y - l.p1.y) * r
    return L2Distance(p, Point(px, py))


def MoveAlongAngle(nowPos, angle, dis):

    dx = 1.0 * dis * math.cos(angle)
    dy = 1.0 * dis * math.sin(angle)

    return nowPos + Point(dx, dy)


def DisFireballHuman(f1, f2, h1, h2):
    h2 = h2 - (f2 - f1)
    return DisLinePoint(Line(h1, h2), f1)


def LegalPos(pos, walls):
    if not PointInRectangle(pos, Wall(0, width, 0, height)):
        return False
    for wall in walls:
        if PointInRectangle(pos, wall):
            return False
    return True

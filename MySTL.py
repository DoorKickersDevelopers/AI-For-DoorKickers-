#                             _ooOoo_
#                            o8888888o
#                            88" . "88
#                            (| -_- |)
#                            O\  =  /O
#                         ____/`---'\____
#                       .'  \\|     |//  `.
#                      /  \\|||  :  |||//  \
#                     /  _||||| -:- |||||-  \
#                     |   | \\\  -  /// |   |
#                     | \_|  ''\---/''  |   |
#                     \  .-\__  `-`  ___/-. /
#                   ___`. .'  /--.--\  `. . __
#                ."" '<  `.___\_<|>_/___.'  >'"".
#               | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#               \  \ `-.   \_ __\ /__ _/   .-` /  /
#          ======`-.____`-.___\_____/___.-`____.-'======
#                             `=---='
#          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                      God Bless Me, No Bugs.

import math
from math import sqrt,fabs,atan2
import Arguments



# When I wrote this,only God and I understood what I was doing


class Point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point({},{})".format(self.x,self.y)

    def __add__(self,other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self,other):
        return Point(self.x-other.x, self.y-other.y)

    def __mul__(self,other):
        return self.x*other.y-self.y*other.x

    def __eq__(self,other):
        return self.x==other.x and self.y==other.y



class Line(object):
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        if p1==p2:
            raise Exception("create an instance of line with illegal argument")
    def Points(self):
        return self.p1,self.p2
    def __str__(self):
        return "Line( {} , {} )".format(self.p1.__str__(),self.p2.__str__())
    def __eq__(self,other):
        return self.p1==other.p1 and self.p2==other.p2

class Rectangle(object):
    def __init__(self,left,right,bottom,top):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        if self.right<=self.left or self.top<=self.bottom:
            raise Exception("create an instance of Rectangle with illegal argument")
    def __str__(self):
        return "Rect(x:[{},{}],y:[{},{}])".format(self.left,self.right,self.bottom,self.top)
    def Points(self):
        return Point(self.left, self.bottom),Point(self.left, self.top),Point(self.right, self.bottom),Point(self.right, self.top)
    def __eq__(self,other):
        return self.left==other.left and self.right==other.right and self.bottom==other.bottom and self.top==other.top

    def Lines(self):
        p1,p2,p3,p4 = Points()
        return Line(p1, p2),Line(p1, p3),Line(p2, p4),Line(p3, p4)

    def expand(self,d):
        return Rectangle(self.left-d, self.right+d, self.bottom-d, self.top+d)


class Circle(object):
    def __init__(self,centre,radius):
        self.centre = centre
        self.radius = radius
        if self.radius<=0:
            raise Exception("create an instance of Circle with illegal radius")
    def __str__(self):
        return "Circle(o:{},r:{})".format(self.centre,self.radius)
    def __eq__(self,other):
        return self.centre==other.centre and self.radius==other.radius



def L2Distance(p1,p2):
    """
    Point p1
    Point p2
    return Euclidean Distance
    """
    return sqrt((p1.x-p2.x)*(p1.x-p2.x)+(p1.y-p2.y)*(p1.y-p2.y))



def PointInRectangle(p,rect):
    """
    Point p
    Rectangle rect
    return True if p in rect(containing no edges)
    """
    return (rect.left<p.x and p.x<rect.right) and (rect.bottom<p.y and p.y<rect.top)

def RectangleIntersection(rect1,rect2):
    """
    Rectangle rect1
    Rectangle rect2
    return True if rect1 intersect with rect2(containing no edges)
    """
    
    eps = 1e-6


    smallrect1 = Rectangle(rect1.left+eps, rect1.right-eps, rect1.bottom+eps, rect1.top-eps)
    smallrect2 = Rectangle(rect2.left+eps, rect2.right-eps, rect2.bottom+eps, rect2.top-eps)

    ret = False

    p1,p2,p3,p4 = smallrect1.Points()
    ret = ret or PointInRectangle(p1, rect2) or PointInRectangle(p2, rect2) or PointInRectangle(p3, rect2) or PointInRectangle(p4, rect2)
    
    p1,p2,p3,p4 = smallrect2.Points()
    ret = ret or PointInRectangle(p1, rect1) or PointInRectangle(p2, rect1) or PointInRectangle(p3, rect1) or PointInRectangle(p4, rect1)

    return ret

def PointOnLine(p,l):
    """
    Point p
    Line l 
    return True if p on l
    """
    eps = 1e-9
    return fabs(L2Distance(l.p1,p)+L2Distance(l.p2, p)-L2Distance(l.p1, l.p2))<eps



def LineIntersection(l1,l2):
    '''
    Line l1
    Line l2
    return True if l1 intersect with l2 (have an intersection)
    '''

    def Rect(line):
        return Rectangle(min(line.p1.x,line.p2.x), max(line.p1.x,line.p2.x), min(line.p1.y,line.p2.y), max(line.p1.y,line.p2.y))

    if not RectangleIntersection(Rect(l1), Rect(l2)):
        return False

    if PointOnLine(l1.p1, l2) or PointOnLine(l1.p2, l2) or PointOnLine(l2.p1, l1) or PointOnLine(l2.p2, l1):
        return True

    p1 = l1.p2-l1.p1

    if ((l2.p1-l1.p1)*p1)*((l2.p2-l1.p1)*p1)>=0:
        return False

    p2 = l2.p2-l2.p1

    if ((l1.p1-l2.p1)*p2)*((l1.p2-l2.p1)*p2)>=0:
        return False

    return True

    #This Implementation is slow, maybe bugs exist
    #Fix later 

def RotateTo(angle1, angle2):
    '''
    float angle1
    float angle2
    return rot degree if you want to rotate from rot1 to rot2
    Warning: No cliping with Human_Rot_Max
    '''
    if 0<=angle1 and angle1 <= 180:
        if angle2>angle1+180:
            return -(angle1+360-angle2)
        return angle2-angle1
    if angle1 >= 180:
        if angle2<angle1-180:
            return 360-angle1+angle2
        return angle2-angle1

def Angle(p1,p2):
    '''
    Point p1
    Point p2
    return Angle(p2-p1)
    '''
    if p1==p2:
        raise Exception("Try to get Angle with illegal Argument")
    p = p2-p1
    angle = atan2(p.y, p.x)
    angle = angle/math.pi*180
    if angle<0 :
        return angle+360
    else:
        return angle

def LineIntersectRect(l,rect):
    '''
    Line l
    Rectangle rect
    return True if l intersect with rect(contain no edge)
    '''
    if PointInRectangle(l.p1, rect) or PointInRectangle(l.p2,rect):
        return True

    eps = 1e-5

    smallrect = Rectangle(rect.left+eps, rect.right-eps, rect.bottom+eps, rect.top-eps)
    p1,p2,p3,p4 = smallrect.Points()
    l1,l2,l3,l4 = Line(p1, p2),Line(p1, p3),Line(p2, p4),Line(p3, p4)

    return LineIntersection(l, l1) or LineIntersection(l, l2) or LineIntersection(l, l3) or LineIntersection(l, l4)


def DisLinePoint(l,p):
    '''
    Line l
    Point p
    return p to line dis
    '''
    dot = (l.p2.x-l.p1.x)*(p.x-l.p1.x)+(l.p2.y-l.p1.y)*(p.y-l.p1.y)
    d2 = (l.p2.x-l.p1.x)*(l.p2.x-l.p1.x)+(l.p2.y-l.p1.y)*(l.p2.y-l.p1.y)
    if dot<=0:
        return L2Distance(p, l.p1)
    if dot>=d2:
        return L2Distance(p, l.p2)

    r = dot/d2
    px = l.p1.x + ( l.p2.x - l.p1.x ) *r
    py = l.p1.y + ( l.p2.y - l.p1.y ) *r
    return sqrt( (p.x - px)*(p.x - px) + (p.y - py)*(p.y - py))


def CircleIntersectLine(c,l):
    '''
    Circle c
    Line l
    return True if c intersect with l (more than one intersection)
    '''
    eps = 1e-5
    if DisLinePoint(l,c.centre)<c.radius-eps:
        return True
    else:
        return False

def MoveAlongAngle(nowPos,angle,dis):
    '''
    Point nowPos
    float angle
    float dis
    return pos where nowPos move by dis along angle
    '''
    angle = 1.0*angle/180*math.pi
    dx = 1.0*dis*math.cos(angle)
    dy = 1.0*dis*math.sin(angle)

    pos = nowPos+Point(dx, dy)
    return pos



def FutureGrenadePos(grenade,walls,future):
    if grenade.time<future:
        return None,None
    pos1 = bullet.position
    angle = bullet.rotation
    angle = 1.0*angle/180*math.pi
    dx = 1.0*bullet.velocity*future*math.cos(angle)
    dy = 1.0*bullet.velocity*future*math.sin(angle)
    pos2 = pos1+Point(dx, dy)
    #TODO:



    

def FutureBulletPos(bullet,walls,future):
    pos1 = bullet.position
    angle = bullet.rotation
    angle = 1.0*angle/180*math.pi
    dx = 1.0*bullet.velocity*future*math.cos(angle)
    dy = 1.0*bullet.velocity*future*math.sin(angle)
    pos2 = pos1+Point(dx, dy)
    if pos2.x<map_lbx or pos2.x>map_rbx or pos2.y<map_lby or pos2.y>map_rby:
        return None

    line = Line(pos1, pos2)
    r = bullet.radius
    eps = 1e-5
    for wall in walls:
        ps = wall.Points()
        for p in ps:
            dis = DisLinePoint(line, p)
            if dis < bullet.radius-eps:
                return None
        rect = wall.expand(-eps)
        l1,l2,l3,l4 = wall.Lines()
        if  LineIntersection(l1, line) or LineIntersection(l2, line) or LineIntersection(l3, line) or LineIntersection(l4, line):
            return None
        if DisLinePoint(l1, pos2)<bullet.radius or DisLinePoint(l2, pos2)<bullet.radius or DisLinePoint(l3, pos2)<bullet.radius or DisLinePoint(l4, pos2)<bullet.radius:
            return None
    return pos2



def FutureWeaponMap(walls,bullets,grenades,future):
    '''
    list of Wall: walls
    list of Bullet : bullets
    list of Grenade : grenades
    int : future

    return ball,walls,bullets,humans,grenades whose pos in future turns  
    
    e.g. future = 1 : next turn

    Warning: assume human has no influence , so does ball 
    '''
    nowBullets = []
    nowGrenades = []

    for bullet in bullets:
        pos = FutureBulletPos(bullet, walls, future)
        if pos != None:
            nowBullet = Bullet(pos,bullet.rotation)
            nowBullets.append(nowBullet) 

    for grenade in grenades:
        pos,rot = FutureGrenadePos(grenade, walls, future)
        if pos != None:
            nowGrenade = Grenade(pos,rot,grenade.time-future)
            nowGrenades.append(nowGrenade)

    return nowBullets,nowGrenades



# Now, God only knows

if __name__ == '__main__':
    p1 = Point(0, 0)
    p2 = Point(0, 1)
    p3 = Point(1, 0)
    p4 = Point(1, 1)
     
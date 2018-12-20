import math
from math import sqrt,fabs,atan2

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


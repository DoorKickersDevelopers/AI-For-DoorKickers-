from AI_Player import AI_player
from math import sqrt,atan2,degrees,fabs
import queue
from pygame.draw import line

red = (255,0,0)


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


eps = 5

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


class MyAI(AI_player):
    

    def __init__(self,num,ball,wall,bul,human,gre,screen):
        super().__init__(num,ball,wall,bul,human,gre)
        self.screen = screen

    @staticmethod
    def dis(Pos1,Pos2):
        return sqrt(Pos1.distance_square(Pos2))

    @staticmethod
    def getAngle(Pos1,Pos2):
        Pos = dot(Pos2.x-Pos1.x, Pos2.y-Pos1.y)
        angle = atan2(Pos.y,Pos.x)
        angle = degrees(angle)
        if(angle<0):
            angle += 360
        return angle 
    def InWall(self,Pos,Wall):
        return (Wall.left<=Pos.x and Pos.x<=Wall.right) and (Wall.bottom<=Pos.y and Pos.y<= Wall.top)


    def NoWallOnTheWay(self,Pos):
        me = self.humans[self.number]

        density = 10
        deltax = Pos.x-me.position.x
        deltay = Pos.y-me.position.y
        deltax /= density 
        deltay /= density

        


        for i in range(density):
            Pos.x-=deltax
            Pos.y-=deltay
            for wall in self.wall:
                if self.InWall(Pos, wall):
                    return False

        return True


    def RotateTo(self,Pos):
        angle1 = self.humans[self.number].rotation
        angle2 = self.getAngle(self.humans[self.number].position,Pos)
        print(self.number,angle1,angle2)
        def min(a,b):
            if a>b :
                return b
            else:
                return a

        if 0<=angle1 and angle1 <= 180:
            if angle2>angle1+180:
                return (1,-min(human_rotate_max,angle1+360-angle2),0,False,False)
            if angle2<angle1:
                return (1,-min(human_rotate_max,angle1-angle2),0,False,False)
            return (1,min(human_rotate_max,angle2-angle1),0,False,False)
        if angle1 >= 180:
            if angle2>angle1:
                return (1,min(human_rotate_max, angle2-angle1),0,False,False)
            if angle2<angle1-180:
                return (1,min(human_rotate_max, 360-angle1+angle2),0,False,False)
            return (1,-min(human_rotate_max, angle1-angle2),0,False,False)

    def Survival(self):
        mind = 1e9
        Pos = None
        me = self.humans[self.number]
        for bullet in self.bullets:
            if self.dis(bullet.position,me.position)< mind:
                mind = self.dis(bullet.position,me.position)
                Pos = bullet.position
        for human in self,humans:
            if self.dis(human.position,me.position)<mind and human.number!=self.number:
                mind = self.dis(human.position,me.position)
                Pos = human.position

        for grenade in self.grenades:
            if self.dis(grenade.position,me.position)<mind:
                mind = self.dis(grenade.position,me.position)
                Pos = grenade.position

        ag = self.getAngle(me.position,Pos)






        if fabs(ag-me.rotation)<eps or 360-fabs(ag-me.rotation)<eps:
            return (2,0,-human_speed_max,False,False)
        else:
            ag = 360 - ag
            if fabs(ag-me.rotation)<eps or 360-fabs(ag-me.rotation)<eps:
                return (2,0,human_speed_max,False,False)
            else:
                return self.RotateTo(Pos)


    class Point:
        def __init__(self,x,y,number):
            self.x = x
            self.y = y
            self.num = number
            self.next = []
            self.dis = 1e9
            self.pre = None
        def addedge(self,point):
            self.next.append(point)
        def distance_square(self, o):
            return (self.x - o.x) * (self.x - o.x) + (self.y - o.y) * (self.y - o.y)


    def Goto(self,Pos):
        Nodes = []
        me = self.humans[self.number]
        Nodes.append(self.Point(me.position.x,me.position.y,0))
        num = 0
        for wall in self.wall:
            num += 1
            Nodes.append(self.Point(wall.right+human_r,wall.top+human_r,num))
            num += 1
            Nodes.append(self.Point(wall.right+human_r,wall.bottom-human_r,num))
            num += 1
            Nodes.append(self.Point(wall.left-human_r,wall.top+human_r,num))
            num += 1
            Nodes.append(self.Point(wall.left-human_r,wall.bottom-human_r,num))
        num+=1

        #print(self.number,Nodes)

        def Intersect(pos1,pos2):
            density = 10
            deltax = 1.0*(pos2.x-pos1.x)/density
            deltay = 1.0*(pos2.y-pos1.y)/density
            
            for i in range(density+1):
                pos = dot(pos1.x+deltax*i, pos1.y+deltay*i)
                for wall in self.wall:
                    if self.InWall(pos,wall):
                        return True
            #if(self.number==0):
            #    line(self.screen, red, (pos1.x,pos1.y), (pos2.x,pos2.y), 1)
            return False

        
        Nodes.append(self.Point(Pos.x,Pos.y,num))
        for i in range(len(Nodes)):
            for j in range(len(Nodes)):
                if i!=j and not Intersect(Nodes[i],Nodes[j]):
                    Nodes[i].addedge(Nodes[j])
                    #line(self.screen, red, (Nodes[i].x,Nodes[i].y), (Nodes[j].x,Nodes[j].y), 1)

        q = queue.Queue()

        q.put_nowait(Nodes[0])

        Nodes[0].dis = 0

        while not q.empty():
            x = q.get_nowait()
            for nextnode in x.next:
                if nextnode.dis > x.dis + self.dis(x,nextnode):
                    nextnode.dis = x.dis + self.dis(x,nextnode)
                    nextnode.pre = x
                    q.put_nowait(nextnode)

        x = Nodes[-1]
        while (x.pre!=Nodes[0]):
            x = x.pre
            if x==None:
                print("Error! Not Connected!")
                break
        if x == Nodes[-1]:
            print(self.number,"can see Target")

        if fabs(self.getAngle(me.position,x)-me.rotation)<eps or 360-fabs(self.getAngle(me.position,x)-me.rotation)<eps:
            return (2,0,human_speed_max,False,False)
        
        ang = 360-me.rotation

        if fabs(self.getAngle(me.position,x)-ang)<eps or 360-fabs(self.getAngle(me.position,x)-ang)<eps:
            return (2,0,-human_speed_max,False,False)

        return self.RotateTo(x)
        

    def analysis(self):
        '''
        self.number : int 
        self.humans : []
        Human : position,rotation hp grenade_number fire_time node  
        self.ball : position belong=-1
        self.grenades []
        Grenade : position velocity time
        self.bullets : position velocity
        self.wall : []
        Rect : left right top bottom 
        '''
        if self.ball.belong == self.number: 
            return self.Survival()

        if self.ball.belong == -1:
            return self.Goto(self.ball.position)

        me = self.humans[self.number]


        
        limit = 40

        if (self.ball.belong!=-1) and (self.ball.belong!=self.number):
            if (self.NoWallOnTheWay(self.ball.position) and (self.dis(me.position,self.ball.position)<=limit)) and (me.fire_time==0 or me.grenade_number>0):
                if fabs(self.getAngle(me.position,self.ball.position)-self.rotation)<eps or 360-fabs(self.getAngle(me.position,self.ball.position)-self.rotation)<eps:
                    if me.fire_time==0:
                        return (3,0,0,True,False)
                    if me.grenade_number>0:
                        return (4,0,0,False,True)
                else:
                    self.RotateTo(self.ball.position)
            else:
                self.Goto(self.ball.position)



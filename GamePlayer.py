import pygame
from pygame import Rect
import sys
import random
import copy
import time
import json
from BaseClass import *
from MySTL import *

filedir = "log.json"


def draw_rectangle(screen, rect, color):
    pygame.draw.rect(screen, color, pygame.Rect(int(rect.left), int(rect.bottom), int(rect.right - rect.left),
                                                int(rect.top - rect.bottom)))


def draw_circle(screen, circ, color):
    pygame.draw.circle(screen, color, (int(circ.centre.x),
                                       int(circ.centre.y)), int(circ.radius))


def draw_human(screen, human):
    # print("Shit!")
    r = human_radius
    p = human.circle.centre
    draw_circle(screen, human.circle, red)
    newp = MoveAlongAngle(p, human.rotation, 2 * human_radius)
    pygame.draw.line(screen, red, (p.x, p.y), (newp.x, newp.y), 4)
    myfont = pygame.font.Font(None, 20)
    textImage = myfont.render(str(human.hp), True, black)
    screen.blit(textImage, (human.circle.centre.x, human.circle.centre.y))


def PlayJsonFile(mydir):
    pygame.init()
    screen = pygame.display.set_mode((width_of_screen, height_of_screen))
    pygame.display.set_caption("Door Kickers Player")
    with open(mydir, "r")as file:
        Json = file.read().replace("None", "null")
        Json = json.loads(Json)

    walls = json.loads(Json[0]["walls"])
    num_of_walls = len(walls)
    for i in range(num_of_walls):
        walls[i] = Wall(walls[i][0], walls[i][1],
                        walls[i][2], walls[i][3])

    Score = Json[-1]["scores"]
    Json = Json[1:-1]
    timecnt = 0
    for frame in Json:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        humans = json.loads(frame["humans"])
        num_of_humans = len(humans)
        for i in range(num_of_humans):
            if humans[i] == None:
                continue
            num = humans[i][0]
            pos = Point(humans[i][1][0], humans[i][1][1])
            rot = humans[i][2]
            hp = humans[i][3]
            humans[i] = Human(pos, rot, num)
            humans[i].hp = hp

        meteors = json.loads(frame["meteors"])
        num_of_meteors = len(meteors)
        for i in range(num_of_meteors):
            pos = Point(meteors[i][0][0], meteors[i][0][1])
            meteors[i] = Meteor(pos)

        fireballs = json.loads(frame["fireballs"])
        num_of_fireballs = len(fireballs)
        for i in range(num_of_fireballs):
            pos = Point(fireballs[i][0][0], fireballs[i][0][1])
            fireballs[i] = Fireball(pos)

        ball = json.loads(frame["balls"])
        ball = Point(ball[0][0], ball[0][1])
        ball = Ball(ball)
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

        events = json.loads(frame["events"])
        if len(events) > 0:
            print(
                "=====================time = {} frames=====================".format(timecnt))
        timecnt += 1
        for event in events:
            if event[0] == 1:
                print("Player {} shoots!".format(event[1]))
            elif event[0] == 2:
                print("Player {} gets {} hurt!".format(event[1], event[2]))
            elif event[0] == 3:
                print("Player {} died!".format(event[1]))
            elif event[0] == 4:
                print("Player {} cast Meteor!".format(event[1]))
            elif event[0] == 5:
                print("Player {} gets ball!".format(event[1]))
            elif event[0] == 6:
                print("A Fireball splashes at ({},{})!".format(
                    event[1], event[2]))
            elif event[0] == 7:
                print("A Meteor impacts at ({},{})!".format(
                    event[1], event[2]))
            elif event[0] == 8:
                print("Player {} reincarnate at ({},{})!".format(
                    event[1], event[2], event[3]))
            elif event[0] == 9:
                print("A Fireball disappears at ({},{})!".format(
                    event[1], event[2]))

        time.sleep(1.0 / 25)

    print("=====================score board=====================")

    for i, s in enumerate(Score):
        print("Player{} :".format(i), s)
    print("=====================================================")


if __name__ == "__main__":
    PlayJsonFile(filedir)

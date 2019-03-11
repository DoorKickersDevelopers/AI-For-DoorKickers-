import pygame
import sys
import random
import copy
import time
import json
from BaseClass import *


def PlayJsonFile(mydir):
    print()
    print("Load Replay File={}".format(mydir))

    with open(mydir, "r")as file:
        Json = file.read()
        Json = json.loads(Json)
    init_info = Json[0]
    final_info = Json[-1]
    Json = Json[1:-1]
    MapID = init_info["map"]
    map_dir = "." + os.sep + "Maps" + os.sep
    map_names = os.listdir(map_dir)
    map_names.sort()
    map_name = map_names[MapID]
    with open(map_dir + map_name, "r")as file:
        JSON = file.read()
        JSON = json.loads(JSON)
    width = JSON["width"]
    height = JSON["height"]
    faction_number = JSON["faction_number"]
    birth_places = JSON["birth_places"]
    ball_places = JSON["ball_places"]
    target_places = JSON["target_places"]
    wallrects = JSON["walls"]
    human_number = JSON["human_number"]

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Defense Of The sOgou")

    def draw_wall(wall):
        pygame.draw.rect(screen, black, pygame.Rect(int(wall.left), int(wall.bottom),
                                                    int(wall.right - wall.left), int(wall.top - wall.bottom)))

    def draw_ball(ball):
        pygame.draw.circle(screen, green, (int(ball.pos.x),
                                           int(ball.pos.y)), int(ball.radius))

    def draw_fireball(fireball):
        pygame.draw.circle(screen, red, (int(fireball.pos.x),
                                         int(fireball.pos.y)), int(fireball.radius))

    def draw_target(target):
        pygame.draw.circle(screen, gray, (int(target.pos.x),
                                          int(target.pos.y)), int(target.radius))

    def draw_meteor(meteor):
        pygame.draw.circle(screen, pink, (int(meteor.pos.x), int(
            meteor.pos.y)), int(meteor.attack_radius))

    def draw_human(human):
        if human.inv_time > 0:
            pygame.draw.circle(screen, golden, (int(human.pos.x), int(
                human.pos.y)), int(fireball_radius + 3))
        pygame.draw.circle(screen, blue, (int(human.pos.x),
                                          int(human.pos.y)), int(fireball_radius))
        myfont = pygame.font.Font(None, 20)
        textImage = myfont.render(str(human.hp), True, blue)
        screen.blit(textImage, (human.pos.x, human.pos.y))

    def draw_all(humans, walls, balls, fireballs, meteors, targets):
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        for target in targets:
            draw_target(target)
        for meteor in meteors:
            draw_meteor(meteor)
        for wall in walls:
            draw_wall(wall)
        for human in humans:
            if human.death_time == -1:
                draw_human(human)
        for fireball in fireballs:
            draw_fireball(fireball)
        for ball in balls:
            draw_ball(ball)
        pygame.display.flip()

    walls = [Wall(w[0], w[1], w[2], w[3]) for w in wallrects]
    targets = [TargetArea(Point(t[0], t[1])) for t in target_places]

    humans = [None] * faction_number * human_number
    balls = [None] * faction_number

    for fac, birth_place in enumerate(birth_places):
        for i, pos in enumerate(birth_place):
            humans[i * faction_number +
                   fac] = Human(i * faction_number + fac, Point(pos[0], pos[1]))
            humans[i * faction_number + fac].reset()
    for fac, ball_place in enumerate(ball_places):
        balls[fac] = Ball(Point(ball_place[0], ball_place[1]), fac)
        balls[fac].reset()

    for Data in Json:
        timecnt = Data['frame']
        hs = json.loads(Data["humans"])
        for i in range(faction_number * human_number):
            num = hs[i][0]
            h = humans[i]
            h.pos = Point(hs[i][1], hs[i][2])
            h.hp, h.meteor_num, h.meteor_time, h.flash_num, h.flash_time, h.fireball_time, h.death_time, h.inv_time = tuple(
                hs[i][3:])

        meteors = json.loads(Data["meteors"])
        num_of_meteors = len(meteors)
        for i in range(num_of_meteors):
            pos = Point(meteors[i][0], meteors[i][1])
            lasttime = meteors[i][2]
            from_number = meteors[i][3]
            meteors[i] = Meteor(pos, from_number)
            meteors[i].time = lasttime

        fireballs = json.loads(Data["fireballs"])
        num_of_fireballs = len(fireballs)
        for i in range(num_of_fireballs):
            pos = Point(fireballs[i][0], fireballs[i][1])
            rot = fireballs[i][2]
            from_number = fireballs[i][3]
            fireballs[i] = Fireball(pos, rot, from_number)

        bs = json.loads(Data["balls"])
        for i in range(faction_number):
            pos = Point(bs[i][0], bs[i][1])
            balls[i].pos = pos
            balls[i].belong = bs[i][2]
            balls[i].faction = bs[i][3]

        draw_all(humans, walls, balls, fireballs, meteors, targets)

        events = json.loads(Data["events"])
        if len(events) > 0:
            print(
                "=====================time = {} frames=====================".format(timecnt))

        for event in events:
            if event[0] == 1:
                print("Player {} shoots!".format(event[1]))
            elif event[0] == 2:
                print("Player {} gets {} hurt from {}!".format(
                    event[1], event[2], event[3]))
            elif event[0] == 3:
                print("Player {} died at ({},{})!".format(
                    event[1], event[2], event[3]))
            elif event[0] == 4:
                print("Player {} cast Meteor!".format(
                    event[1]))
            elif event[0] == 5:
                print("Player {} gets ball!".format(
                    event[1]))
            elif event[0] == 6:
                print("A Fireball from {} splashes at ({},{})!".format(
                    event[3], event[1], event[2]))
            elif event[0] == 7:
                print("A Meteor from {} impacts at ({},{})!".format(
                    event[3], event[1], event[2]))
            elif event[0] == 8:
                print("Player {} reincarnate!".format(
                    event[1]))
            elif event[0] == 9:
                print("Player {} flashes from ({},{}) to ({},{})!".format(
                    event[1], event[2], event[3], event[4], event[5]))
            elif event[0] == 10:
                print("Player {} goals with faction{}'s ball!".format(
                    event[1], event[2]))

        time.sleep(1.0 / 25)

    print("=====================score board=====================")

    for i, s in enumerate(json.loads(final_info["scores"])):
        print("Player{} :".format(i), s)
    print("=====================================================")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        PlayJsonFile(sys.argv[1])
    else:
        replay_dir = "." + os.sep + "Replay" + os.sep
        replay_names = os.listdir(replay_dir)
        if len(replay_names) == 0:
            raise Exception("No Replay File in default dir")

        def TimeStampToTime(timestamp):
            timeStruct = time.localtime(timestamp)
            return timeStruct

        def get_FileModifyTime(filePath):
            t = os.path.getmtime(filePath)
            return TimeStampToTime(t)

        newest_t = get_FileModifyTime(replay_dir + replay_names[0])
        name = replay_names[0]

        for replay_name in replay_names[1:]:
            T = get_FileModifyTime(replay_dir + replay_name)
            if newest_t < T:
                newest_t = T
                name = replay_name
        PlayJsonFile(replay_dir + name)

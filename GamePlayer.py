import pygame
import sys
import random
import copy
import time
import json
from BaseClass import *


def PlayJsonFile(mydir):
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

    with open(mydir, "r")as file:
        Json = file.read()
        Json = json.loads(Json)
    init_info = Json[0]
    final_info = Json[-1]
    Json = Json[1:-1]
    MapID = init_info
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
            rot = fireballs[i][1]
            fireballs[i] = Fireball(pos, rot)

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

        time.sleep(1.0 / 25)

    print("=====================score board=====================")

    for i, s in enumerate(Score):
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
            filePath = unicode(filePath, 'utf8')
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

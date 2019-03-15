import os
import random
import json
import numpy as np
# some constants about pygame
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
golden = (217, 217, 25)
gray = (127, 127, 127)
purple = (255, 0, 255)
pink = (242, 156, 177)


# game setting
friendly_fire = True

# load the map,assert the map's legality
map_dir = "." + os.sep + "Maps" + os.sep
map_names = os.listdir(map_dir)
map_names.sort()
map_id = random.randint(0, len(map_names) - 1)
map_name = map_names[map_id]
with open(map_dir + map_name, "r")as file:
    JSON = file.read()
    JSON = json.loads(JSON)
width = JSON["width"]
height = JSON["height"]
faction_number = JSON["faction_number"]
birth_places = JSON["birth_places"]
ball_places = JSON["ball_places"]
target_places = JSON["target_places"]
walls = JSON["walls"]
walls = np.asarray(walls).astype(np.bool)
human_number = JSON["human_number"]
room_size = 200


# some constants about time
frames_per_second = 20
frames_of_game = JSON["time_of_game"] * frames_per_second
time_of_round = 1.0 / frames_per_second
frames_of_death = 5 * frames_per_second
frames_of_invincible = 2 * frames_per_second


# some constants about human
human_hp = 100
human_meteor_number = 3
human_flash_number = 3
human_fireball_interval = frames_per_second * 1
human_meteor_interval = frames_per_second * 3
human_flash_interval = frames_per_second * 3
human_velocity = 5

# some constants about skills
fireball_velocity = 4
fireball_radius = 5
splash_radius = 8
splash_hurt = 10

meteor_distance = 300
meteor_delay = frames_per_second * 2
explode_radius = 100
explode_hurt = 50

flash_distance = 200

# some constants about balls
ball_radius = 5

# some constants about target district
target_radius = 50

# some constants about score
kill_score = 5
killed_score = 0
goal_score = 20
goaled_score = 0

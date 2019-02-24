black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

density_of_wall = 0.45
max_num_of_wall = 15
room_size = 20


height_of_screen = 600
width_of_screen = 800

map_lbx = 0
map_ubx = width_of_screen
map_lby = 0
map_uby = height_of_screen


frames_per_second = 20
human_hp = 100
human_meteor_number = 3
human_fireball_interval = frames_per_second * 1
human_meteor_interval = frames_per_second * 3
human_radius = 10
human_speed_max = 5
human_rotate_max = 10

velocity_of_fireball = 4
fireball_radius = 5
splash_radius = fireball_radius + 2 * human_speed_max
fireball_hurt = 10

cast_distance = 300
meteor_delay = frames_per_second * 2

explode_radius = 50
explode_hurt = 50

ball_radius = 5

time_of_game = 20 * frames_per_second
time_of_round = 1.0 / frames_per_second
time_of_death = 5 * frames_per_second

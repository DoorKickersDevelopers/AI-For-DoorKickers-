#pragma once

//常数都放在这里

namespace CONST {
	const double density_of_wall = 0.45;
	const int max_num_of_wall = 15;
	const double room_size = 20;
	const double height_of_screen = 600;
	const double width_of_screen = 800;
	const double map_lbx = 0;
	const double map_ubx = width_of_screen;
	const double map_lby = 0;
	const double map_uby = height_of_screen;
	const int frames_per_second = 20;
	const int human_hp = 100;
	const int human_meteor_number = 3;
	const int human_fireball_interval = frames_per_second * 1;
	const int human_meteor_interval = frames_per_second * 3;
	const double human_radius = 10;
	const double human_speed_max = 2;
	const double human_rotate_max = 10;
	const double velocity_of_fireball = 4;
	const double fireball_radius = 5;
	const double splash_radius = fireball_radius + 2 * human_speed_max;
	const int fireball_hurt = 10;
	const double cast_distance = 200;
	const int meteor_delay = frames_per_second * 4;
	const double explode_radius = 50;
	const int explode_hurt = 50;
	const double ball_radius = 5;
	const int time_of_game = 3 * frames_per_second;
}
#pragma once

//常数都放在这里

namespace CONST {
	const int frames_per_second = 20;
	const double time_of_round = 1.0 / frames_per_second;
	const int frames_of_death = 5 * frames_per_second;
	const int frames_of_invincible = 2 * frames_per_second;

	const int human_hp = 100;
	const int human_meteor_number = 3;
	const int human_flash_number = 3;
	const int human_fireball_interval = frames_per_second * 1;
	const int human_meteor_interval = frames_per_second * 3;
	const int human_flash_interval = frames_per_second * 3;
	const double human_velocity = 5;

	const double fireball_velocity = 4;
	const double fireball_radius = 5;
	const double splash_radius = 8;
	const int splash_hurt = 10;

	const double meteor_distance = 300;
	const int meteor_delay = frames_per_second * 2;
	const double explode_radius = 100;
	const int explode_hurt = 50;

	const double flash_distance = 200;

	const double ball_radius = 5;

	const double target_radius = 50;

	const int kill_score = 5;
	const int killed_score = 0;
	const int goal_score = 20;
	const int goaled_score = 0;


}
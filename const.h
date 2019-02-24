#pragma once

//常数都放在这里

namespace CONST {
	const double density_of_wall = 0.45;//生成墙的密度
	const int max_num_of_wall = 15;//墙的最大数目
	const double room_size = 20;//生成墙时的单元方块像素数，建议选手忽略以上常数
	const double height_of_screen = 600;//屏幕高度
	const double width_of_screen = 800;//屏幕宽度
	const int frames_per_second = 20;//帧率
	const int human_hp = 100;//最大血量
	const int human_meteor_number = 3;//初始陨石数目
	const int human_fireball_interval = frames_per_second * 1;//开火冷却时间
	const int human_meteor_interval = frames_per_second * 3;//陨石冷却时间
	const double human_radius = 10;//玩家的半径
	const double human_speed_max = 2;//玩家最大移动速度
	const double human_rotate_max = 10;//玩家最大旋转速度
	const double velocity_of_fireball = 4;//火球移动速度
	const double fireball_radius = 5;//火球半径
	const double splash_radius = fireball_radius + 2 * human_speed_max;//火球命中目标后爆裂半径
	const int fireball_hurt = 10;//单个火球伤害
	const double cast_distance = 200;//陨石施法最远距离
	const int meteor_delay = frames_per_second * 4;//陨石从发出到造成伤害的间隔
	const double explode_radius = 50;//陨石爆炸半径
	const int explode_hurt = 50;//陨石爆炸伤害
	const double crystal_radius = 5;//水晶半径
	const int time_of_game = 3 * frames_per_second;//游戏总时长
}
#pragma once

//��������������

namespace CONST {
	const double density_of_wall = 0.45;//����ǽ���ܶ�
	const int max_num_of_wall = 15;//ǽ�������Ŀ
	const double room_size = 20;//����ǽʱ�ĵ�Ԫ����������������ѡ�ֺ������ϳ���
	const double height_of_screen = 600;//��Ļ�߶�
	const double width_of_screen = 800;//��Ļ���
	const int frames_per_second = 20;//֡��
	const int human_hp = 100;//���Ѫ��
	const int human_meteor_number = 3;//��ʼ��ʯ��Ŀ
	const int human_fireball_interval = frames_per_second * 1;//������ȴʱ��
	const int human_meteor_interval = frames_per_second * 3;//��ʯ��ȴʱ��
	const double human_radius = 10;//��ҵİ뾶
	const double human_speed_max = 2;//�������ƶ��ٶ�
	const double human_rotate_max = 10;//��������ת�ٶ�
	const double velocity_of_fireball = 4;//�����ƶ��ٶ�
	const double fireball_radius = 5;//����뾶
	const double splash_radius = fireball_radius + 2 * human_speed_max;//��������Ŀ����Ѱ뾶
	const int fireball_hurt = 10;//���������˺�
	const double cast_distance = 200;//��ʯʩ����Զ����
	const int meteor_delay = frames_per_second * 4;//��ʯ�ӷ���������˺��ļ��
	const double explode_radius = 50;//��ʯ��ը�뾶
	const int explode_hurt = 50;//��ʯ��ը�˺�
	const double crystal_radius = 5;//ˮ���뾶
	const int time_of_game = 3 * frames_per_second;//��Ϸ��ʱ��
}
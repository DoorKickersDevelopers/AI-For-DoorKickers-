#pragma once

#include "const.h"
#include "geometry.h"

#include <vector>
using namespace std;
using namespace CONST;

/*
//ǽ�࣬�������������ĸ��ߵ�λ����Ϣ���������±ߵ�λ��ָ�����꣬���ұߵ�λ��ָ�����ꡣ
class Wall {
public:
	vector<vector<bool>> pixels;
	
	Wall(){}
	Wall(double l, double r, double b, double t):
		left(l),right(r),bottom(b),top(t){}
};
*/

//�����,����ʱhpΪ0
class Human {
public:
	int number;//���
	Point position;//λ��
	int hp;//����ֵ
	int meteor_number;//ʣ�µ���ʯ����
	int meteor_time;//��ʯ��ʣ����ȴʱ��
	int flash_num;//ʣ����������
	int flash_time;//����ʣ����ȴʱ��
	int fire_time;//������ȴʣ��ʱ��
	int death_time;//����ʣ��ʱ��
	int inv_time;//�޵�ʱ��

	Human(int n, double x, double y, int h, int mn, int mt, int fn, int ft, int fit, int dt, int it):
		number(n), position(Point(x, y)), hp(h), meteor_number(mn), meteor_time(mt), 
		flash_num(fn), flash_time(ft), fire_time(fit), death_time(dt), inv_time(it){
		}
	Human(){}
};

//������
class Fireball {
public:
	Point position;//λ��
	double rotation;//����
	int from_number;//�����ĸ���
	
	Fireball(){}
	Fireball(double x, double y, double r, int f):
		position(Point(x, y)), rotation(r), from_number(f){}
};

//��ʯ��
class Meteor {
public:
	Point position;//����λ��
	int last_time;//ʣ�����ʱ��
	int from_number;//�����ĸ���
	
	Meteor(){}
	Meteor(double x, double y, int t, int f):
		position(Point(x, y)), last_time(t), from_number(f){}
};

//ˮ����
class Crystal {
public:
	Point position;//λ��
	int belong;//����(ָ������)
	int faction;//��������
	
	Crystal(double x, double y, int n, int f):
		position(Point(x, y)), belong(n), faction(f){}
	Crystal(){}
	
};

class Operation {
public:
	int flag;
	vector<Point> move;
	vector<Point> shoot;
	vector<Point> meteor;
	vector<bool> flash;
};

class Map {
public:
	int width;//��
	int height;//��
	int faction_number;//��������
	int human_number;//ÿ�����������˵ĸ���
	vector<vector<Point>> birth_places;//ÿ���˵ĳ�����
	vector<Point> crystal_places;//ÿ��������ˮ����ʼλ��
	vector<Point> target_places;//ÿ��������ˮ������Ŀ��λ��
	vector<Point> bonus_places;//ÿ���ӷֵ��ߵ�λ��
	//vector<Wall> walls;//ǽ
	vector<vector<bool>> pixels;//��Ϸ��ͼ��������Ϣ��(x, y)��Ϊtrue��ʾ[x,x+1]��[y,y+1]������ǽ
	int time_of_game;//��Ϸ��ʱ��

	Map() {};
	void set(int w, int h, int f, int hn, vector<vector<Point>> b, vector<Point> c, vector<Point> t, vector<Point> bo, vector<vector<bool>> p, int ti) {
		width = w;
		height = h;
		faction_number = f;
		human_number = hn;
		birth_places = b;
		crystal_places = c;
		target_places = t;
		bonus_places = bo;
		//walls = wa;
		pixels = p;
		time_of_game = ti;
	}
};

//�������࣬�ں�������Ҫ������
class Logic {
private:
	static Logic* instance;
	Logic() {};
	Logic(Logic const&) {};
public:
	int frame;//���ڵ�֡��
	Map map;//��ͼ
	int faction;//�Լ��ı��
	//vector<Wall> walls;
	vector<Human> humans;//������
	vector<Fireball> fireballs;//���л���
	vector<Meteor> meteors;//������ʯ
	vector<Crystal> crystal;//����ˮ��
	vector<bool> bonus;//�ӷֵ����Ƿ����(���Ա��Ե�)

	Operation ope;//���ξ��߲����ļ��ϣ�ѡ�ֿ��Ժ���

	//LogicΪ�����࣬��ʹ��Logic::Instance()��ȡָ��
	static Logic* Instance() {
		if (Logic::instance == 0) {
			Logic::instance = new Logic();
		}
		return Logic::instance;
	}

	void move(int num, Point p);//ָ������Ƶĵ�num�����ƶ���pλ��
	void shoot(int num, Point p);//ָ������Ƶĵ�num������pλ�÷������
	void meteor(int num, Point p);//ָ������Ƶĵ�num������pλ���ͷ���ʯ��
	void flash(int num);//ָ������Ƶĵ�num���˱����ƶ���Ϊ����
	void unmove(int num);//ȡ������Ƶĵ�num���˵��ƶ�ָ��
	void unshoot(int num);//ȡ������Ƶĵ�num���˵����ָ��
	void unmeteor(int num);//ȡ������Ƶĵ�num���˵ķ�����ʯָ��
	void unflash(int num);//ȡ������Ƶĵ�num���˵�����ָ��

	bool isWall(int x, int y);
	
	//��������º���
	void initMap(int w, int h, int f, int hn, vector<vector<Point>> b, vector<Point> c, vector<Point> t, vector<Point> bo, vector<vector<bool>> p, int ti);
	void getFrame(int frame, vector<Human> h, vector<Fireball> b, vector<Meteor> g, vector<Crystal> ba, vector<bool> bo);
	void resetOpe();
};

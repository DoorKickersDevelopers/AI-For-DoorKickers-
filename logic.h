#pragma once

#include "const.h"
#include "geometry.h"

#include <vector>
using namespace std;
using namespace CONST;


//ǽ�࣬�������������ĸ��ߵ�λ����Ϣ���������±ߵ�λ��ָ�����꣬���ұߵ�λ��ָ�����ꡣ
class Wall {
public:
	double left, right, bottom, top;
	
	Wall(){}
	Wall(double l, double r, double b, double t):
		left(l),right(r),bottom(b),top(t){}
};

//�����,����ʱhpΪ0
class Human {
public:
	int number;//���
	Point position;//λ��
	int hp;//����ֵ
	int meteor_number;//ʣ�µ���ʯ����
	int meteor_time;
	int flash_num;
	int flash_time;
	int fire_time;//������ȴʣ��ʱ��
	int death_time;
	int inv_time;

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
	int from_number;
	
	Fireball(){}
	Fireball(double x, double y, double r, int f):
		position(Point(x, y)), rotation(r), from_number(f){}
};

//��ʯ��
class Meteor {
public:
	Point position;//����λ��
	int last_time;//ʣ�����ʱ��
	int from_number;
	
	Meteor(){}
	Meteor(double x, double y, int t, int f):
		position(Point(x, y)), last_time(t), from_number(f){}
};

//ˮ����
class Crystal {
public:
	Point position;//λ��
	int belong;//����
	int faction;
	
	Crystal(double x, double y, int n, int f):
		position(Point(x, y)), belong(n), faction(f){}
	Crystal(){}
	
};

//������
/*
 *"flag": 1/2/3/4,		//�ֱ��ʾ��ǰ�ƶ�/��ת/������/�콵����
 *"args": "[x,y]/[rot,]/[]/[x,y]",		  //ϣ���ƶ����ĵص㣬���ܳ�������ƶ�����/��ת�Ƕ�/������/�콵����	 		
 */
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
	int width;
	int height;
	int faction_number;
	int human_number;
	vector<vector<Point>> birth_places;
	vector<Point> crystal_places;
	vector<Point> target_places;
	vector<Wall> walls;
	int time_of_game;

	Map() {};
	void set(int w, int h, int f, int hn, vector<vector<Point>> b, vector<Point> c, vector<Point> t, vector<Wall> wa, int ti) {
		width = w;
		height = h;
		faction_number = f;
		human_number = hn;
		birth_places = b;
		crystal_places = c;
		target_places = t;
		walls = wa;
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
	int frame;
	Map map;
	int faction;//�Լ��ı��
	//vector<Wall> walls;
	vector<Human> humans;
	vector<Fireball> fireballs;
	vector<Meteor> meteors;
	vector<Crystal> crystal;

	Operation ope;

	//LogicΪ�����࣬��ʹ��Logic::Instance()��ȡָ��
	static Logic* Instance() {
		if (Logic::instance == 0) {
			Logic::instance = new Logic();
		}
		return Logic::instance;
	}

	void move(int num, Point p);
	void shoot(int num, Point p);
	void meteor(int num, Point p);
	void flash(int num);
	void unmove(int num);
	void unshoot(int num);
	void unmeteor(int num);
	void unflash(int num);
	
	//��������º���
	void initMap(int w, int h, int f, int hn, vector<vector<Point>> b, vector<Point> c, vector<Point> t, vector<Wall> wa, int ti);
	void getFrame(int frame, vector<Human> h, vector<Fireball> b, vector<Meteor> g, vector<Crystal> ba);
	void resetOpe();
};

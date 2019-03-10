#pragma once

#include "const.h"
#include "geometry.h"

#include <vector>
using namespace std;
using namespace CONST;


//墙类，包含上下左右四个边的位置信息，其中上下边的位置指纵坐标，左右边的位置指横坐标。
class Wall {
public:
	double left, right, bottom, top;
	
	Wall(){}
	Wall(double l, double r, double b, double t):
		left(l),right(r),bottom(b),top(t){}
};

//玩家类,死亡时hp为0
class Human {
public:
	int number;//编号
	Point position;//位置
	int hp;//生命值
	int meteor_number;//剩下的陨石数量
	int meteor_time;
	int flash_num;
	int flash_time;
	int fire_time;//开火冷却剩余时间
	int death_time;
	int inv_time;

	Human(int n, double x, double y, int h, int mn, int mt, int fn, int ft, int fit, int dt, int it):
		number(n), position(Point(x, y)), hp(h), meteor_number(mn), meteor_time(mt), 
		flash_num(fn), flash_time(ft), fire_time(fit), death_time(dt), inv_time(it){
		}
	Human(){}
};

//火球类
class Fireball {
public:
	Point position;//位置
	double rotation;//朝向
	int from_number;
	
	Fireball(){}
	Fireball(double x, double y, double r, int f):
		position(Point(x, y)), rotation(r), from_number(f){}
};

//陨石类
class Meteor {
public:
	Point position;//中心位置
	int last_time;//剩余存在时间
	int from_number;
	
	Meteor(){}
	Meteor(double x, double y, int t, int f):
		position(Point(x, y)), last_time(t), from_number(f){}
};

//水晶类
class Crystal {
public:
	Point position;//位置
	int belong;//归属
	int faction;
	
	Crystal(double x, double y, int n, int f):
		position(Point(x, y)), belong(n), faction(f){}
	Crystal(){}
	
};

//操作类
/*
 *"flag": 1/2/3/4,		//分别表示向前移动/旋转/发火球/天降正义
 *"args": "[x,y]/[rot,]/[]/[x,y]",		  //希望移动到的地点，不能超过最大移动距离/旋转角度/无意义/天降正义	 		
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

//总数据类，内含所有需要的数据
class Logic {
private:
	static Logic* instance;
	Logic() {};
	Logic(Logic const&) {};
public:
	int frame;
	Map map;
	int faction;//自己的编号
	//vector<Wall> walls;
	vector<Human> humans;
	vector<Fireball> fireballs;
	vector<Meteor> meteors;
	vector<Crystal> crystal;

	Operation ope;

	//Logic为单例类，请使用Logic::Instance()获取指针
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
	
	//请忽略以下函数
	void initMap(int w, int h, int f, int hn, vector<vector<Point>> b, vector<Point> c, vector<Point> t, vector<Wall> wa, int ti);
	void getFrame(int frame, vector<Human> h, vector<Fireball> b, vector<Meteor> g, vector<Crystal> ba);
	void resetOpe();
};

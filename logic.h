#pragma once

#include "const.h"
#include "geometry.h"

#include <vector>
using namespace std;
using namespace CONST;

class Wall {
public:
	int left, right, bottom, top;
	
	Wall(){}
	Wall(int l,int r,int b,int t):
		left(l),right(r),bottom(b),top(t){}
};

class Human {
public:
	int number;
	Point position;
	double rotation;
	int hp;
	int grenade_number;
	int fire_time;
	
	Human(int n, double x, double y, double r, int h, int g, int t):
		number(n), position(Point(x, y)), rotation(r), hp(h), grenade_number(g), fire_time(t){
		}
	Human(){}
};

class Bullet {
public:
	Point position;
	double rotation;
	
	Bullet(){}
	Bullet(double x, double y, double r):
		position(Point(x, y)), rotation(r){}
};

class Grenade {
public:
	Point position;
	double rotation;
	int lasttime;
	
	Grenade(){}
	Grenade(double x, double y, int t):
		position(Point(x, y)), lasttime(t){}
};

class Ball {
public:
	Point position;
	int belong;
	
	Ball(double x, double y, int n):
		position(Point(x, y)), belong(n){
		}
	Ball(){
	}
	
};

class Event {
public:
	int opt;
	union {
		int number;
		struct {
			int number;
			int hurt;
		}onehurt;
		struct{
			double x;
			double y;
		}pos;
	}arg;
};

class Operation {
public:
	int flag;
	double arg1, arg2; 
};

class Logic {
public:
	vector<Wall> walls;
	vector<Human> humans;
	vector<Bullet> bullets;
	vector<Grenade> grenades;
	Ball ball;
	vector<Event> events;
	//vector<vector<Event>> replay;
	static Logic* instance;
	Logic() {};
	Logic(Logic const&){};

public:
	static Logic* Instance() {
		if (Logic::instance == 0) {
			Logic::instance = new Logic();
		}
		return Logic::instance;
	}
	
	void init(vector<Wall> w);
	
	void getmess(vector<Human> h, vector<Bullet> b, vector<Grenade> g, Ball ba, vector<Event> e);
};

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
	double rotation;//朝向
	int hp;//生命值
	int meteor_number;//剩下的陨石数量
	int fire_time;//开火冷却剩余时间
	
	Human(int n, double x, double y, double r, int h, int g, int t):
		number(n), position(Point(x, y)), rotation(r), hp(h), meteor_number(g), fire_time(t){
		}
	Human(){}
};

//火球类
class Fireball {
public:
	Point position;//位置
	double rotation;//朝向
	
	Fireball(){}
	Fireball(double x, double y, double r):
		position(Point(x, y)), rotation(r){}
};

//陨石类
class Meteor {
public:
	Point position;//中心位置
	int lasttime;//剩余存在时间
	
	Meteor(){}
	Meteor(double x, double y, int t):
		position(Point(x, y)), lasttime(t){}
};

//水晶类
class Crystal {
public:
	Point position;//位置
	int belong;//归属
	
	Crystal(double x, double y, int n):
		position(Point(x, y)), belong(n){
		}
	Crystal(){
	}
	
};

//操作类
/*
 *"flag": 1/2/3/4,		//分别表示向前移动/旋转/发火球/天降正义
 *"args": "[dis,]/[rot,]/[]/[x,y]",		  //移动距离/旋转角度/无意义/天降正义	 		
 */
class Operation {
public:
	int flag;//操作类型
	double arg1, arg2; //操作参数
};

//总数据类，内含所有需要的数据
class Logic {
private:
	static Logic* instance;
	Logic() {};
	Logic(Logic const&) {};
public:
	int number;//自己的编号
	vector<Wall> walls;
	vector<Human> humans;
	vector<Fireball> fireballs;
	vector<Meteor> meteors;
	Crystal crystal;

	//Logic为单例类，请使用Logic::Instance()获取指针
	static Logic* Instance() {
		if (Logic::instance == 0) {
			Logic::instance = new Logic();
		}
		return Logic::instance;
	}
	
	//请忽略以下函数
	void init(vector<Wall> w);
	void getmess(vector<Human> h, vector<Fireball> b, vector<Meteor> g, Crystal ba);
};

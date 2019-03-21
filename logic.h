#pragma once

#include "const.h"
#include "geometry.h"

#include <vector>
using namespace std;
using namespace CONST;

/*
//墙类，包含上下左右四个边的位置信息，其中上下边的位置指纵坐标，左右边的位置指横坐标。
class Wall {
public:
	vector<vector<bool>> pixels;
	
	Wall(){}
	Wall(double l, double r, double b, double t):
		left(l),right(r),bottom(b),top(t){}
};
*/

//玩家类,死亡时hp为0
class Human {
public:
	int number;//编号
	Point position;//位置
	int hp;//生命值
	int meteor_number;//剩下的陨石数量
	int meteor_time;//陨石术剩余冷却时间
	int flash_num;//剩余闪现数量
	int flash_time;//闪现剩余冷却时间
	int fire_time;//开火冷却剩余时间
	int death_time;//死亡剩余时间
	int inv_time;//无敌时间

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
	int from_number;//来自哪个人
	
	Fireball(){}
	Fireball(double x, double y, double r, int f):
		position(Point(x, y)), rotation(r), from_number(f){}
};

//陨石类
class Meteor {
public:
	Point position;//中心位置
	int last_time;//剩余存在时间
	int from_number;//来自哪个人
	
	Meteor(){}
	Meteor(double x, double y, int t, int f):
		position(Point(x, y)), last_time(t), from_number(f){}
};

//水晶类
class Crystal {
public:
	Point position;//位置
	int belong;//归属(指被扛起)
	int faction;//所属势力
	
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
	int width;//宽
	int height;//高
	int faction_number;//势力个数
	int human_number;//每个势力控制人的个数
	vector<vector<Point>> birth_places;//每个人的出生地
	vector<Point> crystal_places;//每个势力的水晶初始位置
	vector<Point> target_places;//每个势力的水晶搬运目标位置
	vector<Point> bonus_places;//每个加分道具的位置
	//vector<Wall> walls;//墙
	vector<vector<bool>> pixels;//游戏地图的像素信息，(x, y)处为true表示[x,x+1]×[y,y+1]处不是墙
	int time_of_game;//游戏总时间

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

//总数据类，内含所有需要的数据
class Logic {
private:
	static Logic* instance;
	Logic() {};
	Logic(Logic const&) {};
public:
	int frame;//现在的帧数
	Map map;//地图
	int faction;//自己的编号
	//vector<Wall> walls;
	vector<Human> humans;//所有人
	vector<Fireball> fireballs;//所有火球
	vector<Meteor> meteors;//所有陨石
	vector<Crystal> crystal;//所有水晶
	vector<bool> bonus;//加分道具是否存在(可以被吃掉)

	Operation ope;//本次决策操作的集合，选手可以忽略

	//Logic为单例类，请使用Logic::Instance()获取指针
	static Logic* Instance() {
		if (Logic::instance == 0) {
			Logic::instance = new Logic();
		}
		return Logic::instance;
	}

	void move(int num, Point p);//指定你控制的第num个人移动到p位置
	void shoot(int num, Point p);//指定你控制的第num个人向p位置发射火球
	void meteor(int num, Point p);//指定你控制的第num个人向p位置释放陨石术
	void flash(int num);//指定你控制的第num个人本次移动改为闪现
	void unmove(int num);//取消你控制的第num个人的移动指令
	void unshoot(int num);//取消你控制的第num个人的射击指令
	void unmeteor(int num);//取消你控制的第num个人的发射陨石指令
	void unflash(int num);//取消你控制的第num个人的闪现指令

	bool isWall(int x, int y);
	
	//请忽略以下函数
	void initMap(int w, int h, int f, int hn, vector<vector<Point>> b, vector<Point> c, vector<Point> t, vector<Point> bo, vector<vector<bool>> p, int ti);
	void getFrame(int frame, vector<Human> h, vector<Fireball> b, vector<Meteor> g, vector<Crystal> ba, vector<bool> bo);
	void resetOpe();
};

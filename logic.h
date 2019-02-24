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
	double rotation;//����
	int hp;//����ֵ
	int meteor_number;//ʣ�µ���ʯ����
	int fire_time;//������ȴʣ��ʱ��
	
	Human(int n, double x, double y, double r, int h, int g, int t):
		number(n), position(Point(x, y)), rotation(r), hp(h), meteor_number(g), fire_time(t){
		}
	Human(){}
};

//������
class Fireball {
public:
	Point position;//λ��
	double rotation;//����
	
	Fireball(){}
	Fireball(double x, double y, double r):
		position(Point(x, y)), rotation(r){}
};

//��ʯ��
class Meteor {
public:
	Point position;//����λ��
	int lasttime;//ʣ�����ʱ��
	
	Meteor(){}
	Meteor(double x, double y, int t):
		position(Point(x, y)), lasttime(t){}
};

//ˮ����
class Crystal {
public:
	Point position;//λ��
	int belong;//����
	
	Crystal(double x, double y, int n):
		position(Point(x, y)), belong(n){
		}
	Crystal(){
	}
	
};

//������
/*
 *"flag": 1/2/3/4,		//�ֱ��ʾ��ǰ�ƶ�/��ת/������/�콵����
 *"args": "[dis,]/[rot,]/[]/[x,y]",		  //�ƶ�����/��ת�Ƕ�/������/�콵����	 		
 */
class Operation {
public:
	int flag;//��������
	double arg1, arg2; //��������
};

//�������࣬�ں�������Ҫ������
class Logic {
private:
	static Logic* instance;
	Logic() {};
	Logic(Logic const&) {};
public:
	int number;//�Լ��ı��
	vector<Wall> walls;
	vector<Human> humans;
	vector<Fireball> fireballs;
	vector<Meteor> meteors;
	Crystal crystal;

	//LogicΪ�����࣬��ʹ��Logic::Instance()��ȡָ��
	static Logic* Instance() {
		if (Logic::instance == 0) {
			Logic::instance = new Logic();
		}
		return Logic::instance;
	}
	
	//��������º���
	void init(vector<Wall> w);
	void getmess(vector<Human> h, vector<Fireball> b, vector<Meteor> g, Crystal ba);
};

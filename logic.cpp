#include "logic.h"
#include <iostream>
using namespace std;

Logic* Logic::instance = 0;

void Logic::init(vector<Wall> w) {
	walls = w;
}

void Logic::getmess(vector<Human> h, vector<Fireball> b, vector<Meteor> g, Crystal ba) {
	humans = h;
	fireballs = b;
	meteors = g;
	crystal = ba;


	/*
	for (int i = 0; i < h.size(); i++) {
		cout << h[i].position.x << ' ' << h[i].position.y << ' ' << h[i].rotation << ' ' << h[i].number << ' ' << h[i].meteor_number << ' ' << h[i].hp << ' ' << h[i].fire_time << endl;
	}
	for (int i = 0; i < b.size(); i++) {
		cout << b[i].position.x << ' ' << b[i].position.y << ' ' << b[i].rotation << endl;
	}
	for (int i = 0; i < g.size(); i++) {
		cout << g[i].lasttime << ' ' << g[i].position.x << endl;
	}
	cout << ba.belong << ' ' << ba.position.x << endl;

	*/

}
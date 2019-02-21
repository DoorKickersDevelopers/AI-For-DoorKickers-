#include "logic.h"

Logic* Logic::instance = 0;

void Logic::init(vector<Wall> w) {
	walls = w;
}

void Logic::getmess(vector<Human> h, vector<Bullet> b, vector<Grenade> g, Ball ba, vector<Event> e) {
	humans = h;
	bullets = b;
	grenades = g;
	ball = ba;
	events = e;
}
#include "const.h"
#include "playerAI.h"
#include "logic.h"
#include "geometry.h"


#include"jsoncpp/json/json.h"
#include<iostream>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>


using namespace std;


char *JsonFile;


void getfile(int len) {
	JsonFile = new char[len + 10];
	fgets(JsonFile, len, stdin);
}

void readWalls(vector<Wall> &w) {

	Json::Reader reader;
	Json::Value root;
	//用reader将文件解析到root，root包含Json中所有子元素
	if (!reader.parse(JsonFile, JsonFile + strlen(JsonFile), root)) {
		cerr << "Parse failed." << endl;
		return;
	}

	Json::Value wall = root["walls"];
	for (int i = 0; i < wall.size(); i++) {
		Wall tem(wall[i][0].asDouble(), wall[i][1].asDouble(), wall[i][2].asDouble(), wall[i][3].asDouble());
		w.push_back(tem);
	}
}

void readMess(vector<Human> &h, vector<Bullet> &b, vector<Grenade> &g, Ball &ba, vector<Event> &e) {
	Json::Reader reader;
	Json::Value root;

	if (!reader.parse(JsonFile, JsonFile + strlen(JsonFile), root)) {
		cerr << "Parse failed." << endl;
		return;
	}

	Json::Value humans = root["humans"];
	for (int i = 0; i < humans.size(); i++) {
		Human tem(humans[i][0].asInt(), humans[i][1][0].asDouble(), humans[i][1][1].asDouble(),
			humans[i][2].asDouble(), humans[i][3].asInt(), humans[i][4].asInt(), humans[i][5].asInt());
		h.push_back(tem);
	}

	Json::Value bullets = root["bullets"];
	for (int i = 0; i < bullets.size(); i++) {
		Bullet tem(bullets[i][0][0].asDouble(), bullets[i][0][1].asDouble(), bullets[i][1].asDouble());
		b.push_back(tem);
	}

	Json::Value grenades = root["grenades"];
	for (int i = 0; i < grenades.size(); i++) {
		Grenade tem(grenades[i][0][0].asDouble(), grenades[i][0][1].asDouble(), grenades[i][1].asInt());
		g.push_back(tem);
	}

	ba.Pointition.x = root["balls"][0][0].asDouble();
	ba.Pointition.y = root["balls"][0][1].asDouble();
	ba.belong = root["balls"][1].asInt();

	Json::Value events = root["events"];
	for (int i = 0; i < events.size(); i++) {
		int j = events[i][0].asInt();
		Event tem;
		tem.opt = j;
		switch (j) {
		case 1:
		case 3:
		case 4:
		case 5:
			tem.arg.number = events[i][1].asInt();
			break;
		case 2:
			tem.arg.onehurt.number = events[i][1].asInt();
			tem.arg.onehurt.hurt = events[i][2].asInt();
			break;
		case 6:
		case 7:
		case 8:
		case 9:
			tem.arg.pos.x = events[i][1].asDouble();
			tem.arg.pos.y = events[i][2].asDouble();
			break;
		}
		e.push_back(tem);
	}
}

int main() {
	Logic* logic = Logic::Instance();

	int len = 0;

	scanf("%d", &len);
	getfile(len);
	vector<Wall> walls;
	readWalls(walls);
	logic->init(walls);

	while (true) {
		scanf("%d", &len);

		vector<Human> humans;
		vector<Bullet> bullets;
		vector<Grenade> grenades;
		Ball ball;
		vector<Event> events;

		readMess(humans, bullets, grenades, ball, events);
		logic->getmess(humans, bullets, grenades, ball, events);

		Operation ope;
		playerAI(ope);
		char s[20];
		switch (ope.flag) {
		case 1:
		case 2:
			sprintf(s, "[%.2lf,],", ope.arg1);
			break;
		case 3:
			sprintf(s, "[],");
			break;
		case 4:
			sprintf(s, "[%d,%d],", ope.arg1, ope.arg2);
			break;
		}
		char out[10000];
		sprintf(out, "\"flag\":%d,\n\"args\":%s", ope.flag, s);
		printf("%d %s", strlen(out), out);

		if (false)
			break;
	}

	return 0;
}
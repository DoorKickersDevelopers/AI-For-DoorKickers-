#include "const.h"
#include "playerAI.h"
#include "logic.h"
#include "geometry.h"


#include "jsoncpp/json/json.h"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <string>
#include <regex>
#include <fstream>

using namespace std;


char *JsonFile;
bool gameover = false;
int jsonlen = 2000;

void quyinhao(string s) {
	//string s = string(JsonFile);
	regex rep("(: )\"(.*?)\"");
	s = regex_replace(s, rep, "$1$2");
	//s = regex_replace(s, regex("None"), "null");
	strcpy(JsonFile, s.c_str());
}

void getfile(int len) {
	fgets(JsonFile, len + 1, stdin);
}

void readMap() {
	Logic* logic = Logic::Instance();

	Json::Reader reader0;
	Json::Value root0;
	if (!reader0.parse(JsonFile, JsonFile + strlen(JsonFile), root0)) {
		cerr << "Parse failed0." << endl;
		return;
	}

	logic->faction = root0["faction"].asInt();
	int map_number = root0["map"].asInt();


	string str;
	ifstream fin;
	fin.open("Maps/" + to_string(map_number) + ".json", ios::in);
	stringstream buf;
	buf << fin.rdbuf();
	str = buf.str();
	//cout << str << endl;
	fin.close();

	Json::Reader reader;
	Json::Value root;
	quyinhao(str);
	//用reader将文件解析到root，root包含Json中所有子元素

	if (!reader.parse(str, root)) {
		cerr << "Parse failed." << endl;
		return;
	}
	/*
	if (!reader.parse(JsonFile, JsonFile + strlen(JsonFile), root)) {
		cerr << "Parse failed0." << endl;
		return;
	}
	*/

	int width = root["width"].asInt();
	int height = root["height"].asInt();
	int faction_number = root["faction_number"].asInt();
	int human_number = root["human_number"].asInt();
	int time_of_game = root["time_of_game"].asInt();

	Json::Value birth_places_raw = root["birth_places"];
	vector<vector<Point>> birth_places;
	for (int i = 0; i < birth_places_raw.size(); i++) {
		vector<Point> one;
		for (int j = 0; j < birth_places_raw[i].size(); i++) {
			Point p(birth_places_raw[i][j][0].asDouble(), birth_places_raw[i][j][1].asDouble());
			one.push_back(p);
		}
		birth_places.push_back(one);
	}

	Json::Value ball_places_raw = root["ball_places"];
	vector<Point> ball_places;
	for (int i = 0; i < ball_places_raw.size(); i++) {
		Point p(ball_places_raw[i][0].asDouble(), ball_places_raw[i][1].asDouble());
		ball_places.push_back(p);
	}
	
	Json::Value target_places_raw = root["target_places"];
	vector<Point> target_places;
	for (int i = 0; i < target_places_raw.size(); i++) {
		Point p(target_places_raw[i][0].asDouble(), target_places_raw[i][1].asDouble());
		target_places.push_back(p);
	}

	Json::Value pixels_raw = root["walls"];
	/*
	vector<Wall> walls;
	for (int i = 0; i < walls_raw.size(); i++) {
		Wall w(walls_raw[i][0].asDouble(), walls_raw[i][1].asDouble(), walls_raw[i][2].asDouble(), walls_raw[i][3].asDouble());
		walls.push_back(w);
	}
	*/
	vector<vector<bool>> pixels;
	for (int i = 0; i < pixels_raw.size(); i++) {
		vector<bool> line;
		for (int j = 0; j < pixels_raw[i].size(); j++) {
			if (pixels_raw[i][j].asInt() == 0)
				line.push_back(true);
			else
				line.push_back(false);
		}
		pixels.push_back(line);
	}

	logic->initMap(width, height, faction_number, human_number, birth_places, ball_places, target_places, pixels, time_of_game);
}

void readFrame() {
	Json::Reader reader;
	Json::Value root;

	quyinhao(string(JsonFile));

	if (!reader.parse(JsonFile, JsonFile + strlen(JsonFile), root)) {
		cerr << "Parse failed1." << endl;
		return;
	}

	int frame = root["frame"].asInt();
	if (frame == -1) {
		gameover = true;
		return;
	}

	vector<Human> humans;
	Json::Value humans_raw = root["humans"];
	for (int i = 0; i < humans_raw.size(); i++) {
		Human tem(humans_raw[i][0].asInt(), humans_raw[i][1].asDouble(), humans_raw[i][2].asDouble(),
			humans_raw[i][3].asInt(), humans_raw[i][4].asInt(), humans_raw[i][5].asInt(), humans_raw[i][6].asInt(),
			humans_raw[i][7].asInt(), humans_raw[i][8].asInt(), humans_raw[i][9].asInt(), humans_raw[i][10].asInt());
		humans.push_back(tem);
	}

	vector<Fireball> fireballs;
	Json::Value fireballs_raw = root["fireballs"];
	for (int i = 0; i < fireballs_raw.size(); i++) {
		Fireball tem(fireballs_raw[i][0].asDouble(), fireballs_raw[i][1].asDouble(), fireballs_raw[i][2].asDouble(), fireballs_raw[i][3].asInt());
		fireballs.push_back(tem);
	}

	vector<Meteor> meteors;
	Json::Value meteors_raw = root["meteors"];
	for (int i = 0; i < meteors_raw.size(); i++) {
		Meteor tem(meteors_raw[i][0].asDouble(), meteors_raw[i][1].asDouble(), meteors_raw[i][2].asInt(), meteors_raw[i][3].asInt());
		meteors.push_back(tem);
	}


	vector<Crystal> crystal;
	Json::Value crystal_raw = root["crystal"];
	for (int i = 0; i < crystal_raw.size(); i++) {
		Crystal tem(crystal_raw[i][0].asDouble(), crystal_raw[i][1].asDouble(), crystal_raw[i][2].asInt(), crystal_raw[i][3].asInt());
		crystal.push_back(tem);
	}

	Logic::Instance()->getFrame(frame, humans, fireballs, meteors, crystal);
}

void readOnce() {
	char lenr[4];
	for (int i = 0; i < 4; i++) {
		scanf("%c", &lenr[i]);
	}
	int len = (unsigned int)((((unsigned int)lenr[3]) & 255) | ((((unsigned int)lenr[2]) & 255) << 8) | ((((unsigned int)lenr[1]) & 255) << 16) | ((((unsigned int)lenr[0]) & 255) << 24));
	if (len > jsonlen) {
		while (jsonlen <= len) {
			jsonlen *= 2;
		}
		delete JsonFile;
		JsonFile = new char[jsonlen];
	}
	getfile(len);
}

void sendMessage(bool gameover = false) {
	Operation ope = Logic::Instance()->ope;
	Json::Value message;
	if (!gameover) {
		Json::Value move;
		for (int i = 0; i < ope.move.size(); i++) {
			Json::Value p;
			p.append(ope.move[i].x);
			p.append(ope.move[i].y);
			move.append(p);
		}
		Json::Value shoot;
		for (int i = 0; i < ope.shoot.size(); i++) {
			Json::Value p;
			p.append(ope.shoot[i].x);
			p.append(ope.shoot[i].y);
			shoot.append(p);
		}		
		Json::Value meteor;
		for (int i = 0; i < ope.meteor.size(); i++) {
			Json::Value p;
			p.append(ope.meteor[i].x);
			p.append(ope.meteor[i].y);
			meteor.append(p);
		}
		Json::Value flash;
		for (int i = 0; i < ope.flash.size(); i++) {
			flash.append(Json::Value(ope.flash[i]));
		}
		message["flag"] = 0;
		message["move"] = move;
		message["shoot"] = shoot;
		message["meteor"] = meteor;
		message["flash"] = flash;
	}
	else {
		message["flag"] = 2;
	}

	Json::FastWriter writer;
	writer.omitEndingLineFeed();
	//string out = message.toStyledString();
	int len = strlen(writer.write(message).c_str());
	unsigned char lenb[4];
	lenb[0] = (unsigned char)(len);
	lenb[1] = (unsigned char)(len >> 8);
	lenb[2] = (unsigned char)(len >> 16);
	lenb[3] = (unsigned char)(len >> 24);
	for (int i = 0; i < 4; i++) {
		printf("%c", lenb[3 - i]);
	}
	printf("%s", writer.write(message).c_str());
	//printf("%s", out);
	cout.flush();
}

int main() {
	JsonFile = new char[jsonlen];
	Logic* logic = Logic::Instance();

	int len = 0;
	char lenr[4];
	for (int i = 0; i < 4; i++) {
		scanf("%c", &lenr[i]);
	}
	len = (unsigned int)((((unsigned int)lenr[3]) & 255) | ((((unsigned int)lenr[2]) & 255) << 8) | ((((unsigned int)lenr[1]) & 255) << 16) | ((((unsigned int)lenr[0]) & 255) << 24));	
	getfile(len);
	readMap();
	
	while (true) {
		rewind(stdin);

		for (int i = 0; i < 4; i++) {
			scanf("%c", &lenr[i]);
		}
		len = (unsigned int)((((unsigned int)lenr[3]) & 255) | ((((unsigned int)lenr[2]) & 255) << 8) | ((((unsigned int)lenr[1]) & 255) << 16) | ((((unsigned int)lenr[0]) & 255) << 24));
		if (len > jsonlen) {
			while (jsonlen <= len) {
				jsonlen *= 2;
			}
			delete JsonFile;
			JsonFile = new char[jsonlen];
		}
		getfile(len);
		readFrame();
		if (gameover) {
			sendMessage(true);
			return 0;
		}
		logic->resetOpe();
		playerAI();
		sendMessage();
	}
	delete JsonFile;

	return 0;
}
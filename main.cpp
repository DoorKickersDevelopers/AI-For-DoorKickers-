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

using namespace std;


char *JsonFile;
bool gameover = false;
int jsonlen = 2000;

void quyinhao() {
	string s = string(JsonFile);
	regex rep("(: )\"(.*?)\"");
	s = regex_replace(s, rep, "$1$2");
	s = regex_replace(s, regex("None"), "null");
	strcpy(JsonFile, s.c_str());
}

void getfile(int len) {
	fgets(JsonFile, len + 1, stdin);
}

void readWalls(vector<Wall> &w) {

	Json::Reader reader;
	Json::Value root;
	quyinhao();
	//用reader将文件解析到root，root包含Json中所有子元素
	if (!reader.parse(JsonFile, JsonFile + strlen(JsonFile), root)) {
		cerr << "Parse failed0." << endl;
		return;
	}
	Json::Value wall = root["walls"];
	for (int i = 0; i < wall.size(); i++) {
		Wall tem(wall[i][0].asDouble(), wall[i][1].asDouble(), wall[i][2].asDouble(), wall[i][3].asDouble());
		w.push_back(tem);
	}

	Logic::Instance()->number = root["number"].asInt();
}

void readMess(vector<Human> &h, vector<Fireball> &b, vector<Meteor> &g, Crystal &ba) {
	Json::Reader reader;
	Json::Value root;

	quyinhao();

	if (!reader.parse(JsonFile, JsonFile + strlen(JsonFile), root)) {
		cerr << "Parse failed1." << endl;
		return;
	}

	if (!root["balls"]) {
		gameover = true;
		return;
	}

	Json::Value humans = root["humans"];
	for (int i = 0; i < humans.size(); i++) {
		Human tem(humans[i][0].asInt(), humans[i][1][0].asDouble(), humans[i][1][1].asDouble(),
			humans[i][2].asDouble(), humans[i][3].asInt(), humans[i][4].asInt(), humans[i][5].asInt());
		h.push_back(tem);
	}

	Json::Value fireballs = root["fireballs"];
	for (int i = 0; i < fireballs.size(); i++) {
		Fireball tem(fireballs[i][0][0].asDouble(), fireballs[i][0][1].asDouble(), fireballs[i][1].asDouble());
		b.push_back(tem);
	}

	Json::Value meteors = root["meteors"];
	for (int i = 0; i < meteors.size(); i++) {
		Meteor tem(meteors[i][0][0].asDouble(), meteors[i][0][1].asDouble(), meteors[i][1].asInt());
		g.push_back(tem);
	}

	ba.position.x = root["balls"][0][0].asDouble();
	ba.position.y = root["balls"][0][1].asDouble();
	ba.belong = root["balls"][1].asInt();

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
	vector<Wall> walls;
	readWalls(walls);
	logic->init(walls);
	
	while (true) {
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
		vector<Human> humans;
		vector<Fireball> fireballs;
		vector<Meteor> meteors;
		Crystal crystal;
		readMess(humans, fireballs, meteors, crystal);
		if (gameover) {
			char finalope[] = "{\"flag\": 5, \"args\": [0,0]}";
			int len = strlen(finalope);
			unsigned char lenb[4];
			lenb[0] = (unsigned char)(len);
			lenb[1] = (unsigned char)(len >> 8);
			lenb[2] = (unsigned char)(len >> 16);
			lenb[3] = (unsigned char)(len >> 24);
			for (int i = 0; i < 4; i++) {
				printf("%c", lenb[3 - i]);
			}
			printf("%s", finalope);
			cout.flush();
			return 0;
		}
		logic->getmess(humans, fireballs, meteors, crystal);

		Operation ope;
		playerAI(ope);
		char s[20];
		switch (ope.flag) {
		case 1:
			sprintf(s, "[%.2f,%.2f]", ope.arg1, ope.arg2);
			break;
		case 2:
			sprintf(s, "[%.2f,0]", ope.arg1);
			break;
		case 3:
			sprintf(s, "[0,0]");
			break;
		case 4:
			sprintf(s, "[%.2f,%.2f]", ope.arg1, ope.arg2);
			break;
		}
		char out[10000];
		sprintf(out, "{\"flag\": %d,\"args\": %s}", ope.flag, s);
		int len = strlen(out);
		unsigned char lenb[4];
		lenb[0] = (unsigned char)(len);
		lenb[1] = (unsigned char)(len >> 8);
		lenb[2] = (unsigned char)(len >> 16);
		lenb[3] = (unsigned char)(len >> 24);
		for (int i = 0; i < 4; i++) {
			printf("%c", lenb[3 - i]);
		}
		printf("%s", out);
		cout.flush();
	}

	return 0;
}
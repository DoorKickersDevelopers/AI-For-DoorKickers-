#include "playerAI.h"
#include <chrono>
#include <thread>

using namespace CONST;

int fcount = 0;

//�����Ҫ��ɸú�����ͨ�����ð˸�ָ����ɾ��ߣ����return���;���
void playerAI() {

	//std::this_thread::sleep_for(std::chrono::milliseconds(200));
	Logic * logic = Logic::Instance();
	/*
	if (fcount < 20) {
		for (int i = 0; i < logic->map.human_number; i++) {
			Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
			logic->move(i, Point(now.x + 1, now.y + 1));
		}

		for (int i = 0; i < logic->map.human_number; i++) {
			Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
			logic->shoot(i, Point(now.x + 100, now.y + 100));
		}

		for (int i = 0; i < logic->map.human_number; i++) {
			Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
			logic->meteor(i, Point(now.x + 1, now.y + 1));
		}


	}
	else if (fcount < 40) {
		for (int i = 0; i < logic->map.human_number; i++) {
			Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
			logic->shoot(i, Point(now.x - 100, now.y - 100));
		}
	}
	else if (fcount < 60) {
		for (int i = 0; i < logic->map.human_number; i++) {
			Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
			logic->meteor(i, Point(now.x + 1, now.y + 1));
		}
	}
	else if (fcount < 80) {
		for (int i = 0; i < logic->map.human_number; i++) {
			//logic->flash(i);
			Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
			logic->move(i, Point(now.x + 10, now.y + 10));
		}
	}
	fcount++;
	*//*
	if(logic->map.bonus_places.size() > 0 && logic->map.bonus_places[0].x > 0 && logic->bonus.size() > 0)
		if (logic->bonus[0])
			for (int i = 0; i < logic->map.human_number; i++) {
				Point now = logic->humans[i * logic->map.faction_number + (1 - logic->faction)].position;
				logic->shoot(i, Point(now.x, now.y));
			}
		else
			for (int i = 0; i < logic->map.human_number; i++) {
				Point now = logic->humans[i * logic->map.faction_number + (logic->faction)].position;
				logic->move(i, Point(now.x + 1, now.y + 1));
			}*/
	/*
	if (logic->crystal[1 - logic->faction].belong < 0) {
		for (int i = 0; i < logic->map.human_number; i++) {
			Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
			logic->move(i, Point(now.x + 5, now.y));
		}
	}
	else if(fcount++ < 10) {
		
		for (int i = 0; i < logic->map.human_number; i++) {
			Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
			logic->move(i, Point(now.x - 5, now.y));
		}
	}
	if (logic->crystal[logic->faction].belong > -1) {
		for (int i = 0; i < logic->map.human_number; i++) {
			Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
			logic->shoot(i, Point(now.x - 5, now.y));
		}
	}
	*//*
	for (int i = 0; i < logic->map.human_number; i++) {
		Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
		logic->move(i, Point(now.x + 3.5, now.y + 3.5));
		logic->meteor(i, Point(logic->frame, -1));
	}*/
	return;
}
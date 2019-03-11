#include "playerAI.h"
#include <chrono>
#include <thread>

using namespace CONST;

int fcount = 61;

//�����Ҫ��ɸú�����ͨ�����ð˸�ָ����ɾ��ߣ����return���;���
void playerAI() {
	Logic * logic = Logic::Instance();
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
			logic->shoot(i, Point(now.x + 100, now.y + 100));
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
			logic->flash(i);
			Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
			logic->move(i, Point(now.x + 10, now.y + 10));
		}
	}
	fcount++;
}
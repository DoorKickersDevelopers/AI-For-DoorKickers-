#include "playerAI.h"
#include <chrono>
#include <thread>

using namespace CONST;

int fcount = 0;

//玩家需要完成该函数，通过修改参数ope实现决策
void playerAI() {
	Logic * logic = Logic::Instance();
	if (fcount < 20) {
		for (int i = 0; i < logic->map.human_number; i++) {
			Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
			logic->move(i, Point(now.x + 1, now.y + 1));
		}
	}
	else if (fcount < 40) {
		for (int i = 0; i < logic->map.human_number; i++) {
			Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
			logic->shoot(i, Point(now.x + 1, now.y + 1));
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
			Point now = logic->humans[i * logic->map.faction_number + logic->faction].position;
			logic->move(i, Point(now.x + 10, now.y + 10));
		}
	}
	fcount++;
}
#include "playerAI.h"
#include <string>
#include <thread>
#include <chrono>

using namespace CONST;

//玩家需要完成该函数，通过调用八个指令完成决策，最后return发送决策
void playerAI() {
	Logic * logic = Logic::Instance();
	if (logic->frame > 10) {
		logic->debug("qweqweqweqwe");
		logic->debugAppend("asdasdasd");
		logic->debug("debug in frame");
		logic->debugAppend(to_string(logic->frame) + " is ok!");
	}
	if (logic->frame > 50) {
		std::this_thread::sleep_for(chrono::milliseconds(303));
	}
	if (logic->frame > 100) {
		for (int i = 0; i < 2000; i++) {
			logic->debugAppend(to_string(i));
		}
	}

	return;
}
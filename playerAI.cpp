#include "playerAI.h"
#include <chrono>
#include <thread>

using namespace CONST;

int fcount = 0;

//�����Ҫ��ɸú�����ͨ���޸Ĳ���opeʵ�־���
void playerAI(Operation& ope) {
	this_thread::sleep_for(chrono::milliseconds(500));
	

	if (fcount < 20) {
		ope.flag = 1;
		ope.arg1 = Logic::Instance()->humans[Logic::Instance()->number].position.x + 1;
		ope.arg2 = Logic::Instance()->humans[Logic::Instance()->number].position.y + 1;
	}
	else if (fcount < 40) {
		ope.flag = 2;
		ope.arg1 = 10;
	}
	else if (fcount < 60) {
		ope.flag = 3;
	}
	else if (fcount < 80) {
		ope.flag = 4;
		ope.arg1 = Logic::Instance()->humans[Logic::Instance()->number].position.x;
		ope.arg2 = Logic::Instance()->humans[Logic::Instance()->number].position.y;
	}
	else {
		fcount = 0;
	}
	fcount++;
}
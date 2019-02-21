#include "playerAI.h"

using namespace CONST;

int fcount = 0;

void playerAI(Operation& ope) {
	if (fcount < 20) {
		ope.flag = 1;
		ope.arg1 = 2;
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
		ope.arg1 = 100;
		ope.arg2 = 200;
	}
	else {
		fcount = 0;
	}
}
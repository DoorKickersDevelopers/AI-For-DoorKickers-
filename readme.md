# 文档

## 文件说明
* **const.h**:常数都在这里。
* **geometry.h & geometry.cpp**:可能用到的计算几何库。
* **logic.h & logic.cpp**:游戏数据类，具体结合游戏说明望文生义即可。其中Logic类中储存了所有需要的数据，使用Logic::Instance()获取单例Logic类指针。
* **playerAI.h & playerAI.cpp**:选手需要完成playerAI函数，函数中通过修改参数ope完成你本帧的操作。具体操作约定见协议约定。
* **main.cpp**:负责网络收发，选手可以忽略这个文件。

## 编译说明
直接make即可，生成可执行文件main.exe。
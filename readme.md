# 文档

## 文件说明
* **const.h**:常数都在这里。
* **geometry.h & geometry.cpp**:可能用到的计算几何库。首先定义了点、线段、直线三种几何结构，然后实现了点、线段、直线、圆等的基本运算。
* **logic.h & logic.cpp**:游戏数据类。包括墙、玩家、火球、陨石、水晶、事件、操作类。其中将所有数据储存在Logic类中(包括自己的编号)，选手需要使用Logic::Instance()获取单例Logic类指针再进一步读取数据。
* **playerAI.h & playerAI.cpp**:选手需要完成void playerAI(Operation& ope)函数，函数中通过修改参数ope完成你本帧的操作。程序保证在调用playerAI函数前已经获取好当前游戏最新的信息，函数结束后方将选手的操作发送出去。允许选手花费若干帧进行一次决策，在函数结束前，选手不会得到新的地图信息，同时选手将处于静止状态。
* **main.cpp**:负责网络收发，选手可以忽略这个文件。

## 常数列表

| 常数类型 | 常数名称 | 数值 | 意义 |
| :------: | :------: | :------: | :------: |
| double | density_of_wall | 0.45 | 生成墙的密度 |
| int | max_num_of_wall | 15 | 墙的最大数目 |
| double | room_size | 20 | 生成墙时的单元方块像素数，建议选手忽略以上常数 |
| double | height_of_screen | 600 | 屏幕高度 |
| double | width_of_screen | 800 | 屏幕宽度 |
| int | frames_per_second | 20 | 帧率 |
| int | human_hp | 100 | 最大血量 |
| int | human_meteor_number | 3 | 初始陨石数目 |
| int | human_fireball_interval | frames_per_second * 1 | 开火冷却时间 |
| int | human_meteor_interval | frames_per_second * 3 | 陨石冷却时间 |
| double | human_radius | 10 | 玩家的半径 |
| double | human_speed_max | 2 | 玩家最大移动速度 |
| double | human_rotate_max | 10 | 玩家最大旋转速度 |
| double | velocity_of_fireball | 4 | 火球移动速度 |
| double | fireball_radius | 5 | 火球半径 |
| double | splash_radius | fireball_radius + 2 * human_speed_max | 火球命中目标后爆裂半径 |
| int | fireball_hurt | 10 | 单个火球伤害 |
| double | cast_distance | 200 | 陨石施法最远距离 |
| int | meteor_delay | frames_per_second * 4 | 陨石从发出到造成伤害的间隔 |
| double | explode_radius | 50 | 陨石爆炸半径 |
| int | explode_hurt | 50 | 陨石爆炸伤害 |
| double | crystal_radius | 5 | 水晶半径 |
| int | time_of_game | 3 * frames_per_second | 游戏总时长 |

## 计算几何库函数列表(具体参数意义参见记返回值意义参见geometry.h，注释比较详细)

函数声明 | 函数意义
:---: | :---:
double dist(Point p1, Point p2) | 返回两点之间欧氏距离
bool equal_Point(Point p1, Point p2) | 判断两个点是否重合
double multiply(Point sp, Point ep, Point op) | 得到(sp-op)和(ep-op)的叉积
double dotmultiply(Point p1, Point p2, Point p0) | 得到矢量(p1-op)和(p2-op)的点积
bool onLine(Lineseg l, Point p) | 判断点p是否在线段l上
Point rotate(Point o, double alpha, Point p) | 返回点p以点o为圆心逆时针旋转alpha弧度后所在的位置
double angle(Point o, Point s, Point e) | 返回顶角在o点，起始边为os，终止边为oe的夹角
double relation(Point p, Lineseg l) | 判断点与线段的关系
Point perpendicular(Point p, Lineseg l) | 求点C到线段AB所在直线的垂足 P
double ptoLinesegdist(Point p, Lineseg l, Point &np) | 求点p到线段l的最短距离,并返回线段上距该点最近的点np
double ptoldist(Point p, Lineseg l) | 求点p到线段l所在直线的距离
double ptoPointset(int vcount, Point Pointset[], Point p, Point &q) | 计算点到折线集的最近距离,并返回最近点
bool CircleInsidePolygon(int vcount, Point center, double radius, Point polygon[]) | 判断圆是否在多边形内
double cosine(Lineseg l1, Lineseg l2) | 返回两个矢量l1和l2的夹角的余弦
double lsangle(Lineseg l1, Lineseg l2) | 返回线段l1与l2之间的夹角
bool intersect(Lineseg u, Lineseg v) | 如果线段u和v相交(包括相交在端点处)时，返回true
bool intersect_A(Lineseg u, Lineseg v) | (线段u和v相交)&&(交点不是双方的端点) 时返回true
bool intersect_l(Lineseg u, Lineseg v) | 线段v所在直线与线段u相交时返回true
Line makeLine(Point p1, Point p2) | 根据已知两点坐标，求过这两点的直线解析方程
double slope(Line l) | 根据直线解析方程返回直线的斜率k
double alpha(Line l) | 返回直线的倾斜角alpha
Point symmetry(Line l, Point p) | 求点p关于直线l的对称点
bool Lineintersect(Line l1, Line l2, Point &p) | 如果两条直线相交，返回true，且返回交点p
bool intersection(Lineseg l1, Lineseg l2, Point &inter) | 如果线段l1和l2相交，返回true且交点由(inter)返回，否则返回false
bool Point_in_circle(Point o, double r, Point p) | 判断点是否在圆内时
int CircleRelation(Point p1, double r1, Point p2, double r2) | 两圆关系
Point rect4th(Point a, Point b, Point c) |  已知矩形的三个顶点，计算第四个顶点d的坐标
bool CircleRecRelation(Point pc, double r, Point pr1, Point pr2, Point pr3, Point pr4) | 判断圆是否在矩形内
bool SameSide(Point p1, Point p2, Line Line) | 点是否在直线同侧


## sdk逻辑说明
首先获取judger发出的初始化信息，然后重复:获取地图信息--调用playerAI函数获取ai决策--发出决策信息的循环。playerAI函数没有运行时间的限制，只有在该函数结束之后才会发出决策信息。如果某几帧ai没有发出决策，那么默认静止。同时每次playerAI函数开始前获取的地图信息都是最新的信息。

## 编译说明
直接make即可，生成可执行文件main.exe。
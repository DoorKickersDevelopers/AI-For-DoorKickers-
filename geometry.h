#pragma once

/* ��Ҫ������ͷ�ļ� */
#include <cmath> 
#include <algorithm>

/* ���õĳ������� */
const double	INF = 1E200;
const double	EP = 1E-10;
const int		MAXV = 300;
const double	PI = 3.14159265;

using namespace std;
/* �������νṹ */

struct Point {
	double x, y;
	Point() {};
	Point(double a, double b) { x = a; y = b; }
};

struct Lineseg {
	Point s;
	Point e;
	Lineseg(Point a, Point b) { s = a; e = b; }
	Lineseg() { }
};

struct Line {         // ֱ�ߵĽ������� a*x+b*y+c=0  Ϊͳһ��ʾ��Լ�� a >= 0 
	double a;
	double b;
	double c;
	Line(double d1 = 1, double d2 = -1, double d3 = 0) { a = d1; b = d2; c = d3; }
};




/**********************
*                    *
*   ��Ļ�������     *
*                    *
**********************/

// ��������֮��ŷ�Ͼ��� 
double dist(Point p1, Point p2); 

// �ж��������Ƿ��غ� 
bool equal_Point(Point p1, Point p2);

/******************************************************************************
r=multiply(sp,ep,op),�õ�(sp-op)��(ep-op)�Ĳ��
r>0��ep��ʸ��opsp����ʱ�뷽��
r=0��opspep���㹲�ߣ�
r<0��ep��ʸ��opsp��˳ʱ�뷽��
*******************************************************************************/
double multiply(Point sp, Point ep, Point op);

/******************************************************************************
r=dotmultiply(p1,p2,op),�õ�ʸ��(p1-op)��(p2-op)�ĵ�����������ʸ��������ʸ��
r<0����ʸ���н�Ϊ��ǣ�
r=0����ʸ���н�Ϊֱ�ǣ�
r>0����ʸ���н�Ϊ�۽�
*******************************************************************************/
double dotmultiply(Point p1, Point p2, Point p0);

/******************************************************************************
�жϵ�p�Ƿ����߶�l��
������(p���߶�l���ڵ�ֱ����) && (��p�����߶�lΪ�Խ��ߵľ�����)
*******************************************************************************/
bool onLine(Lineseg l, Point p);

/******************************************************************************
���ص�p�Ե�oΪԲ����ʱ����תalpha(��λ������)�����ڵ�λ��
*******************************************************************************/
Point rotate(Point o, double alpha, Point p);

/******************************************************************************
���ض�����o�㣬��ʼ��Ϊos����ֹ��Ϊoe�ļн�(��λ������)
�Ƕ�С��pi��������ֵ
�Ƕȴ���pi�����ظ�ֵ
�����������߶�֮��ļн�
ԭ��
r = dotmultiply(s,e,o) / (dist(o,s)*dist(o,e))
r'= multiply(s,e,o)
r >= 1	angle = 0;
r <= -1	angle = -PI
-1<r<1 && r'>0	angle = arccos(r)
-1<r<1 && r'<=0	angle = -arccos(r)
*******************************************************************************/
double angle(Point o, Point s, Point e);


/*****************************\
*                             *
*     �߶μ�ֱ�ߵĻ�������    *
*                             *
\*****************************/


/******************************************************************************
�жϵ����߶εĹ�ϵ
�������Ǹ�������Ĺ�ʽд�ģ�P�ǵ�C���߶�AB����ֱ�ߵĴ���
AC dot AB
r =     ---------
||AB||^2
(Cx-Ax)(Bx-Ax) + (Cy-Ay)(By-Ay)
= -------------------------------
L^2
r has the following meaning:
r=0      P = A
r=1      P = B
r<0		 P is on the backward extension of AB
r>1      P is on the forward extension of AB
0<r<1	 P is interior to AB
*******************************************************************************/
double relation(Point p, Lineseg l);

/******************************************************************************
���C���߶�AB����ֱ�ߵĴ��� P
*******************************************************************************/
Point perpendicular(Point p, Lineseg l);

/******************************************************************************
���p���߶�l����̾���,�������߶��Ͼ�õ�����ĵ�np
ע�⣺np���߶�l�ϵ���p����ĵ㣬��һ���Ǵ���
*******************************************************************************/
double ptoLinesegdist(Point p, Lineseg l, Point &np);

// ���p���߶�l����ֱ�ߵľ���,��ע�Ȿ�������ϸ�����������  
double ptoldist(Point p, Lineseg l);

/* ����㵽���߼����������,�����������.
ע�⣺���õ���ptoLineseg()���� */
double ptoPointset(int vcount, Point Pointset[], Point p, Point &q);

/* �ж�Բ�Ƿ��ڶ������.ptoLineseg()������Ӧ��2 */
bool CircleInsidePolygon(int vcount, Point center, double radius, Point polygon[]);

/* ��������ʸ��l1��l2�ļнǵ�����(-1 --- 1)ע�⣺������������нǵĻ���ע�ⷴ���Һ����Ķ������Ǵ� 0��pi */
double cosine(Lineseg l1, Lineseg l2);
// �����߶�l1��l2֮��ļн� ��λ������ ��Χ(-pi��pi) 
double lsangle(Lineseg l1, Lineseg l2);

//����߶�u��v�ཻ(�����ཻ�ڶ˵㴦)ʱ������true 
//�ж�P1P2����Q1Q2�������ǣ�( P1 - Q1 ) �� ( Q2 - Q1 ) * ( Q2 - Q1 ) �� ( P2 - Q1 ) >= 0��
//�ж�Q1Q2����P1P2�������ǣ�( Q1 - P1 ) �� ( P2 - P1 ) * ( P2 - P1 ) �� ( Q2 - P1 ) >= 0��
bool intersect(Lineseg u, Lineseg v);

//  (�߶�u��v�ཻ)&&(���㲻��˫���Ķ˵�) ʱ����true    
bool intersect_A(Lineseg u, Lineseg v);

// �߶�v����ֱ�����߶�u�ཻʱ����true���������ж��߶�u�Ƿ�����߶�v  
bool intersect_l(Lineseg u, Lineseg v);

// ������֪�������꣬����������ֱ�߽������̣� a*x+b*y+c = 0  (a >= 0)  
Line makeLine(Point p1, Point p2);

// ����ֱ�߽������̷���ֱ�ߵ�б��k,ˮƽ�߷��� 0,��ֱ�߷��� 1e200 
double slope(Line l);

// ����ֱ�ߵ���б��alpha ( 0 - pi) 
double alpha(Line l);

// ���p����ֱ��l�ĶԳƵ�  
Point symmetry(Line l, Point p);

// �������ֱ�� l1(a1*x+b1*y+c1 = 0), l2(a2*x+b2*y+c2 = 0)�ཻ������true���ҷ��ؽ���p  
bool Lineintersect(Line l1, Line l2, Point &p);

// ����߶�l1��l2�ཻ������true�ҽ�����(inter)���أ����򷵻�false 
bool intersection(Lineseg l1, Lineseg l2, Point &inter);

/*************************\
*						 *
* Բ�Ļ�������           *
*					     *
\*************************/
/******************************************************************************
����ֵ	�� ��p��Բ��(�����߽�)ʱ������true
��;	�� ��ΪԲΪ͹���������жϵ㼯�����ߣ�������Ƿ���Բ��ʱ��
ֻ��Ҫ��һ�жϵ��Ƿ���Բ�ڼ��ɡ�
*******************************************************************************/
bool Point_in_circle(Point o, double r, Point p);

//��Բ��ϵ�� 
/* ��Բ��
���룺 return 1��
���У� return 2��
�ཻ�� return 3��
���У� return 4��
�ں��� return 5��
*/
int CircleRelation(Point p1, double r1, Point p2, double r2);

/**************************\
*						  *
* ���εĻ�������          *
*                         *
\**************************/

// ��֪���ε���������(a,b,c)��������ĸ�����d������. ע�⣺��֪�������������������� 
Point rect4th(Point a, Point b, Point c);

/********************\
*				    *
* ����				*
*					*
\********************/

//�ж�Բ�Ƿ��ھ����ڣ�
// �ж�Բ�Ƿ��ھ����ڣ��Ǿͷ���true�������ˮƽ�������ĸ����������Ͽ�ʼ��˳ʱ�����У� =
bool CircleRecRelation(Point pc, double r, Point pr1, Point pr2, Point pr3, Point pr4);

//���Ƿ���ֱ��ͬ�ࣺ
//�������Ƿ���ֱ��ͬ�࣬���򷵻�true 
bool SameSide(Point p1, Point p2, Line Line);


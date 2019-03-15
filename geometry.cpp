#include "geometry.h"


/**********************
*                    *
*   ��Ļ�������     *
*                    *
**********************/

double dist(Point p1, Point p2) {                // ��������֮��ŷ�Ͼ��� 
	return(sqrt((p1.x - p2.x)*(p1.x - p2.x) + (p1.y - p2.y)*(p1.y - p2.y)));
}

bool equal_Point(Point p1, Point p2) {           // �ж��������Ƿ��غ�  
	return ((abs(p1.x - p2.x)<EP) && (abs(p1.y - p2.y)<EP));
}

/******************************************************************************
r=multiply(sp,ep,op),�õ�(sp-op)��(ep-op)�Ĳ��
r>0��ep��ʸ��opsp����ʱ�뷽��
r=0��opspep���㹲�ߣ�
r<0��ep��ʸ��opsp��˳ʱ�뷽��
*******************************************************************************/
double multiply(Point sp, Point ep, Point op) {
	return((sp.x - op.x)*(ep.y - op.y) - (ep.x - op.x)*(sp.y - op.y));
}

/******************************************************************************
r=dotmultiply(p1,p2,op),�õ�ʸ��(p1-op)��(p2-op)�ĵ�����������ʸ��������ʸ��
r<0����ʸ���н�Ϊ��ǣ�
r=0����ʸ���н�Ϊֱ�ǣ�
r>0����ʸ���н�Ϊ�۽�
*******************************************************************************/
double dotmultiply(Point p1, Point p2, Point p0) {
	return ((p1.x - p0.x)*(p2.x - p0.x) + (p1.y - p0.y)*(p2.y - p0.y));
}

/******************************************************************************
�жϵ�p�Ƿ����߶�l��
������(p���߶�l���ڵ�ֱ����) && (��p�����߶�lΪ�Խ��ߵľ�����)
*******************************************************************************/
bool onLine(Lineseg l, Point p) {
	return((multiply(l.e, p, l.s) == 0) && (((p.x - l.s.x)*(p.x - l.e.x) <= 0) && ((p.y - l.s.y)*(p.y - l.e.y) <= 0)));
}

/******************************************************************************
���ص�p�Ե�oΪԲ����ʱ����תalpha(��λ������)�����ڵ�λ��
*******************************************************************************/
Point rotate(Point o, double alpha, Point p) {
	Point tp;
	p.x -= o.x;
	p.y -= o.y;
	tp.x = p.x*cos(alpha) - p.y*sin(alpha) + o.x;
	tp.y = p.y*cos(alpha) + p.x*sin(alpha) + o.y;
	return tp;
}

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
double angle(Point o, Point s, Point e) {
	double cosfi, fi, norm;
	double dsx = s.x - o.x;
	double dsy = s.y - o.y;
	double dex = e.x - o.x;
	double dey = e.y - o.y;

	cosfi = dsx * dex + dsy * dey;
	norm = (dsx*dsx + dsy * dsy)*(dex*dex + dey * dey);
	cosfi /= sqrt(norm);

	if (cosfi >= 1.0) return 0;
	if (cosfi <= -1.0) return -3.1415926;

	fi = acos(cosfi);
	if (dsx*dey - dsy * dex>0) return fi;      // ˵��ʸ��os ��ʸ�� oe��˳ʱ�뷽�� 
	return -fi;
}


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
double relation(Point p, Lineseg l) {
	Lineseg tl;
	tl.s = l.s;
	tl.e = p;
	return dotmultiply(tl.e, l.e, l.s) / (dist(l.s, l.e)*dist(l.s, l.e));
}

/******************************************************************************
���C���߶�AB����ֱ�ߵĴ��� P
*******************************************************************************/
Point perpendicular(Point p, Lineseg l) {
	double r = relation(p, l);
	Point tp;
	tp.x = l.s.x + r * (l.e.x - l.s.x);
	tp.y = l.s.y + r * (l.e.y - l.s.y);
	return tp;
}

/******************************************************************************
���p���߶�l����̾���,�������߶��Ͼ�õ�����ĵ�np
ע�⣺np���߶�l�ϵ���p����ĵ㣬��һ���Ǵ���
*******************************************************************************/
double ptoLinesegdist(Point p, Lineseg l, Point &np) {
	double r = relation(p, l);
	if (r<0) {
		np = l.s;
		return dist(p, l.s);
	}
	if (r>1) {
		np = l.e;
		return dist(p, l.e);
	}
	np = perpendicular(p, l);
	return dist(p, np);
}

// ���p���߶�l����ֱ�ߵľ���,��ע�Ȿ�������ϸ�����������  
double ptoldist(Point p, Lineseg l) {
	return abs(multiply(p, l.e, l.s)) / dist(l.s, l.e);
}

/* ����㵽���߼����������,�����������.
ע�⣺���õ���ptoLineseg()���� */
double ptoPointset(int vcount, Point Pointset[], Point p, Point &q) {
	int i;
	double cd = double(INF), td;
	Lineseg l;
	Point tq, cq;

	for (i = 0; i<vcount - 1; i++) {
		l.s = Pointset[i];

		l.e = Pointset[i + 1];
		td = ptoLinesegdist(p, l, tq);
		if (td<cd) {
			cd = td;
			cq = tq;
		}
	}
	q = cq;
	return cd;
}

/* �ж�Բ�Ƿ��ڶ������.ptoLineseg()������Ӧ��2 */
bool CircleInsidePolygon(int vcount, Point center, double radius, Point polygon[]) {
	Point q;
	double d;
	q.x = 0;
	q.y = 0;
	d = ptoPointset(vcount, polygon, center, q);
	if (d<radius || fabs(d - radius)<EP)
		return true;
	else
		return false;
}

/* ��������ʸ��l1��l2�ļнǵ�����(-1 --- 1)ע�⣺������������нǵĻ���ע�ⷴ���Һ����Ķ������Ǵ� 0��pi */
double cosine(Lineseg l1, Lineseg l2) {
	return (((l1.e.x - l1.s.x)*(l2.e.x - l2.s.x) +
		(l1.e.y - l1.s.y)*(l2.e.y - l2.s.y)) / (dist(l1.e, l1.s)*dist(l2.e, l2.s)));
}

// �����߶�l1��l2֮��ļн� ��λ������ ��Χ(-pi��pi) 
double lsangle(Lineseg l1, Lineseg l2) {
	Point o, s, e;
	o.x = o.y = 0;
	s.x = l1.e.x - l1.s.x;
	s.y = l1.e.y - l1.s.y;
	e.x = l2.e.x - l2.s.x;
	e.y = l2.e.y - l2.s.y;
	return angle(o, s, e);
}

//����߶�u��v�ཻ(�����ཻ�ڶ˵㴦)ʱ������true 
//�ж�P1P2����Q1Q2�������ǣ�( P1 - Q1 ) �� ( Q2 - Q1 ) * ( Q2 - Q1 ) �� ( P2 - Q1 ) >= 0��
//�ж�Q1Q2����P1P2�������ǣ�( Q1 - P1 ) �� ( P2 - P1 ) * ( P2 - P1 ) �� ( Q2 - P1 ) >= 0��
bool intersect(Lineseg u, Lineseg v) {
	return((max(u.s.x, u.e.x) >= min(v.s.x, v.e.x)) &&                     //�ų�ʵ�� 
		(max(v.s.x, v.e.x) >= min(u.s.x, u.e.x)) &&
		(max(u.s.y, u.e.y) >= min(v.s.y, v.e.y)) &&
		(max(v.s.y, v.e.y) >= min(u.s.y, u.e.y)) &&
		(multiply(v.s, u.e, u.s)*multiply(u.e, v.e, u.s) >= 0) &&         //����ʵ�� 
		(multiply(u.s, v.e, v.s)*multiply(v.e, u.e, v.s) >= 0));
}

//  (�߶�u��v�ཻ)&&(���㲻��˫���Ķ˵�) ʱ����true    
bool intersect_A(Lineseg u, Lineseg v) {
	return	((intersect(u, v)) &&
		(!onLine(u, v.s)) &&
		(!onLine(u, v.e)) &&
		(!onLine(v, u.e)) &&
		(!onLine(v, u.s)));
}

// �߶�v����ֱ�����߶�u�ཻʱ����true���������ж��߶�u�Ƿ�����߶�v  
bool intersect_l(Lineseg u, Lineseg v) {
	return multiply(u.s, v.e, v.s)*multiply(v.e, u.e, v.s) >= 0;
}

// ������֪�������꣬����������ֱ�߽������̣� a*x+b*y+c = 0  (a >= 0)  
Line makeLine(Point p1, Point p2) {
	Line tl;
	int sign = 1;
	tl.a = p2.y - p1.y;
	if (tl.a<0) {
		sign = -1;
		tl.a = sign * tl.a;
	}
	tl.b = sign * (p1.x - p2.x);
	tl.c = sign * (p1.y*p2.x - p1.x*p2.y);
	return tl;
}
// ����ֱ�߽������̷���ֱ�ߵ�б��k,ˮƽ�߷��� 0,��ֱ�߷��� 1e200 
double slope(Line l) {
	if (abs(l.a) < 1e-20)
		return 0;
	if (abs(l.b) < 1e-20)
		return INF;
	return -(l.a / l.b);
}
// ����ֱ�ߵ���б��alpha ( 0 - pi) 
double alpha(Line l) {
	if (abs(l.a)< EP)
		return 0;
	if (abs(l.b)< EP)
		return PI / 2;
	double k = slope(l);
	if (k>0)
		return atan(k);
	else
		return PI + atan(k);
}
// ���p����ֱ��l�ĶԳƵ�  
Point symmetry(Line l, Point p) {
	Point tp;
	tp.x = ((l.b*l.b - l.a*l.a)*p.x - 2 * l.a*l.b*p.y - 2 * l.a*l.c) / (l.a*l.a + l.b*l.b);
	tp.y = ((l.a*l.a - l.b*l.b)*p.y - 2 * l.a*l.b*p.x - 2 * l.b*l.c) / (l.a*l.a + l.b*l.b);
	return tp;
}
// �������ֱ�� l1(a1*x+b1*y+c1 = 0), l2(a2*x+b2*y+c2 = 0)�ཻ������true���ҷ��ؽ���p  
bool Lineintersect(Line l1, Line l2, Point &p) {// �� L1��L2  
	double d = l1.a*l2.b - l2.a*l1.b;
	if (abs(d)<EP) // ���ཻ 
		return false;
	p.x = (l2.c*l1.b - l1.c*l2.b) / d;
	p.y = (l2.a*l1.c - l1.a*l2.c) / d;
	return true;
}
// ����߶�l1��l2�ཻ������true�ҽ�����(inter)���أ����򷵻�false 
bool intersection(Lineseg l1, Lineseg l2, Point &inter) {
	Line ll1, ll2;
	ll1 = makeLine(l1.s, l1.e);
	ll2 = makeLine(l2.s, l2.e);
	if (Lineintersect(ll1, ll2, inter))
		return onLine(l1, inter);
	else
		return false;
}

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
bool Point_in_circle(Point o, double r, Point p) {
	double d2 = (p.x - o.x)*(p.x - o.x) + (p.y - o.y)*(p.y - o.y);
	double r2 = r * r;
	return d2<r2 || abs(d2 - r2)<EP;
}


/**************************\
*						  *
* ���εĻ�������          *
*                         *
\**************************/

// ��֪���ε���������(a,b,c)��������ĸ�����d������. ע�⣺��֪�������������������� 
Point rect4th(Point a, Point b, Point c) {
	Point d;
	if (abs(dotmultiply(a, b, c))<EP) { // ˵��c����ֱ�ǹսǴ�
		d.x = a.x + b.x - c.x;
		d.y = a.y + b.y - c.y;
	}
	if (abs(dotmultiply(a, c, b))<EP) { // ˵��b����ֱ�ǹսǴ� 
		d.x = a.x + c.x - b.x;
		d.y = a.y + c.y - b.x;
	}
	if (abs(dotmultiply(c, b, a))<EP) { // ˵��a����ֱ�ǹսǴ� 
		d.x = c.x + b.x - a.x;
		d.y = c.y + b.y - a.y;
	}
	return d;
}

/********************\
*				    *
* ����				*
*					*
\********************/

//��Բ��ϵ�� 
/* ��Բ��
���룺 return 1��
���У� return 2��
�ཻ�� return 3��
���У� return 4��
�ں��� return 5��
*/
int CircleRelation(Point p1, double r1, Point p2, double r2) {
	double d = sqrt((p1.x - p2.x)*(p1.x - p2.x) + (p1.y - p2.y)*(p1.y - p2.y));

	if (fabs(d - r1 - r2) < EP) // ���뱣֤ǰ����if�ȱ��ж��� 
		return 2;
	if (fabs(d - fabs(r1 - r2)) < EP)
		return 4;
	if (d > r1 + r2)
		return 1;
	if (d < fabs(r1 - r2))
		return 5;
	if (fabs(r1 - r2) < d && d < r1 + r2)
		return 3;
	return 0; // indicate an error! 
}
//�ж�Բ�Ƿ��ھ����ڣ�
// �ж�Բ�Ƿ��ھ����ڣ��Ǿͷ���true�������ˮƽ�������ĸ����������Ͽ�ʼ��˳ʱ�����У� 
// ����ptoldist�������ڵ�4ҳ 
bool CircleRecRelation(Point pc, double r, Point pr1, Point pr2, Point pr3, Point pr4) {
	if (pr1.x < pc.x && pc.x < pr2.x && pr3.y < pc.y && pc.y < pr2.y) {
		Lineseg Line1(pr1, pr2);
		Lineseg Line2(pr2, pr3);
		Lineseg Line3(pr3, pr4);
		Lineseg Line4(pr4, pr1);
		if (r<ptoldist(pc, Line1) && r<ptoldist(pc, Line2) && r<ptoldist(pc, Line3) && r<ptoldist(pc, Line4))
			return true;
	}
	return false;
}

//���Ƿ���ֱ��ͬ�ࣺ
//�������Ƿ���ֱ��ͬ�࣬���򷵻�true 
bool SameSide(Point p1, Point p2, Line Line) {
	return (Line.a * p1.x + Line.b * p1.y + Line.c) *
		(Line.a * p2.x + Line.b * p2.y + Line.c) > 0;
}

//���淴���ߣ�
// ��֪�����ߡ����棬�����ߡ� 
// a1,b1,c1Ϊ����ֱ�߷���(a1 x + b1 y + c1 = 0 ,��ͬ)ϵ��;  
//a2,b2,c2Ϊ�����ֱ�߷���ϵ��;  
//a,b,cΪ�����ֱ�߷���ϵ��. 
// �����з���ģ�ʹ��ʱע�⣺���������:<-b2,a2>�����������:<b,-a>. 
// ��Ҫ���ǽ���п��ܻ���"negative zeros" 
void reflect(double a1, double b1, double c1, double a2, double b2, double c2, double &a, double &b, double &c) {
	double n, m;
	double tpb, tpa;
	tpb = b1 * b2 + a1 * a2;
	tpa = a2 * b1 - a1 * b2;
	m = (tpb*b1 + tpa * a1) / (b1*b1 + a1 * a1);
	n = (tpa*b1 - tpb * a1) / (b1*b1 + a1 * a1);
	if (fabs(a1*b2 - a2 * b1)<1e-20) {
		a = a2; b = b2; c = c2;
		return;
	}
	double xx, yy; //(xx,yy)���������뾵��Ľ��㡣 
	xx = (b1*c2 - b2 * c1) / (a1*b2 - a2 * b1);
	yy = (a2*c1 - a1 * c2) / (a1*b2 - a2 * b1);
	a = n;
	b = -m;
	c = m * yy - xx * n;
}

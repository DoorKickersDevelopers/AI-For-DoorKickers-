#pragma once

struct Point {
	double x, y;
	Point(double a = 0, double b = 0) { x = a; y = b; }
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

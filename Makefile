all: main.exe

main.exe: makefile main.o logic.h logic.o Const.h PlayerAI.h PlayerAI.cpp  jsoncpp/json/json-forwards.h jsoncpp/json/json.h jsoncpp/jsoncpp.cpp geometry.o geometry.h
ifeq ($(OS),Windows_NT)
	g++ main.o logic.o PlayerAI.cpp jsoncpp/jsoncpp.cpp geometry.o -o main.exe -D_GLIBCXX_USE_CXX11_ABI=0 -static-libstdc++ -lwsock32 -std=c++11
else
	g++ main.o logic.o PlayerAI.cpp jsoncpp/jsoncpp.cpp geometry.o -o main.exe -D_GLIBCXX_USE_CXX11_ABI=0 -static-libstdc++ -std=c++11
endif

logic.o: makefile Const.h PlayerAI.h geometry.h logic.h jsoncpp/json/json-forwards.h jsoncpp/json/json.h logic.cpp 
	g++ -c logic.cpp -D_GLIBCXX_USE_CXX11_ABI=0 -static-libstdc++ -std=c++11

geometry.o: makefile Const.h PlayerAI.h geometry.h logic.h jsoncpp/json/json-forwards.h jsoncpp/json/json.h geometry.cpp
	g++ -c geometry.cpp -D_GLIBCXX_USE_CXX11_ABI=0 -static-libstdc++ -std=c++11

main.o: makefile Const.h PlayerAI.h geometry.h logic.h jsoncpp/json/json-forwards.h jsoncpp/json/json.h main.cpp
	g++ -c main.cpp -D_GLIBCXX_USE_CXX11_ABI=0 -static-libstdc++ -std=c++11

.PHONY: clean
clean:
	-rm -r *.exe *.o
	-del -r *.exe *.o

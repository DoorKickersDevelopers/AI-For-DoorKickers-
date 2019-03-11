all: main

main: main.o logic.h logic.o const.h playerAI.h playerAI.cpp  jsoncpp/json/json-forwards.h jsoncpp/json/json.h jsoncpp/jsoncpp.cpp geometry.o geometry.h
	g++ main.o logic.o playerAI.cpp jsoncpp/jsoncpp.cpp geometry.o -o main -D_GLIBCXX_USE_CXX11_ABI=0 -static-libstdc++ -std=c++11


logic.o: const.h playerAI.h geometry.h logic.h jsoncpp/json/json-forwards.h jsoncpp/json/json.h logic.cpp
	g++ -c logic.cpp -D_GLIBCXX_USE_CXX11_ABI=0 -static-libstdc++ -std=c++11

geometry.o: const.h playerAI.h geometry.h logic.h jsoncpp/json/json-forwards.h jsoncpp/json/json.h geometry.cpp
	g++ -c geometry.cpp -D_GLIBCXX_USE_CXX11_ABI=0 -static-libstdc++ -std=c++11

main.o: const.h playerAI.h geometry.h logic.h jsoncpp/json/json-forwards.h jsoncpp/json/json.h main.cpp
	g++ -c main.cpp -D_GLIBCXX_USE_CXX11_ABI=0 -static-libstdc++ -std=c++11

.PHONY: clean
clean:
	rm -r main *.o

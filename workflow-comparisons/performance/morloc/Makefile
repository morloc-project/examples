all:
	morloc make main.loc

build:
	gcc -o nexus -O -I/root/.morloc/include nexus.c
	g++ -O3 --std=c++17 -o pool-cpp.out pool.cpp -I/root/.morloc/include -Wall




clean:
	rm -rf nexus nexus.c pool.* __pycache__ log pool-cpp.out

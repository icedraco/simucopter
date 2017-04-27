CC=/usr/bin/g++

EXE=diag

LIB=-lzmq -pthread
FLAGS=-DDIAGNOSTIC

C_FILES=simucopter-agent.cpp bridge.cpp main.cpp
O_FILES=simucopter-requester.o bridge.o main.o

$(EXE): $(O_FILES)
		$(CC) $(FLAGS) -o $(EXE) $^ $(LIB)

.cpp.o:
		$(CC) $(FLAGS) -c -o $@ $^

clean:
		rm -f *.o $(EXE)

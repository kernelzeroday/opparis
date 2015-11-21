CC=g++
CFLAGS=-c -Wall -Wextra -std=c++11
LDFLAGS= `pkg-config --libs opencv` -lopencv_nonfree
SOURCES=$(wildcard *.cpp)
OBJECTS=$(patsubst %.cpp,.obj/%.o,$(SOURCES)) 
EXECUTABLE=flagfinder

all: $(SOURCES) $(EXECUTABLE)
	
$(EXECUTABLE): $(OBJECTS)
	$(CC) -lc $(OBJECTS) $(LDFLAGS) -o $@

.obj/%.o:%.cpp
	$(CC) $(CFLAGS) $< -o $@


clean:
	find . -name \*.o -execdir rm {} \;
	rm -f $(EXECUTABLE)


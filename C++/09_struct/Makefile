CXX = g++
CXXFLAGS = -std=c++23 -Wall -Wextra

TARGET = 09_classes
SRC = 09_classes.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all run clean

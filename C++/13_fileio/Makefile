CXX      = g++
CXXFLAGS = -std=c++23 -Wall -Wextra
TARGET   = 13_fileio
SRC      = 13_fileio.cpp

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $< -o $@

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) *.txt *.bin

.PHONY: run clean

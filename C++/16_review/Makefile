CXX      = g++
CXXFLAGS = -std=c++23 -Wall -Wextra
TARGET   = minecode
SRC      = minecode.cpp

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $< -o $@

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: run clean

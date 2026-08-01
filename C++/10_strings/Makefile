CXX      = g++
CXXFLAGS = -std=c++23 -Wall -Wextra
TARGET   = 10_strings
SRC      = 10_strings.cpp

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $< -o $@

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: run clean

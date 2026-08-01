CXX      = g++
CXXFLAGS = -std=c++23 -Wall -Wextra
TARGET   = 15_string_deeper
SRC      = main.cpp

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $< -o $@

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: run clean

CXX      = g++
CXXFLAGS = -std=c++23 -Wall -Wextra
TARGET   = 11_references
SRC      = 11_references.cpp

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $< -o $@

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: run clean

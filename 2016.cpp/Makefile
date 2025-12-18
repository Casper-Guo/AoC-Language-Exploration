CXX = g++
CXXFLAGS = -std=c++2a
LDFLAGS = -lcrypto

# Default target (optional, prevents running 'make' without args from doing nothing useful)
.PHONY: all clean

# Pattern rule to compile any .cpp file into an executable
# Usage: make day01 (assuming day01.cpp exists)
%: %.cpp utils.cpp
	$(CXX) $^ -o $@ $(CXXFLAGS) $(LDFLAGS)

clean:
	rm -f *.slo *.lo *.o *.obj *.exe *.out test run

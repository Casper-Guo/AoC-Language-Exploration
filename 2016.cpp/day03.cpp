#include "utils.h"

int main() {
  std::ifstream f("input03.txt");
  int side1, side2, side3;

  // part 1
  int possible_count = 0;

  while (f >> side1 >> side2 >> side3) {
    if (side1 + side2 > side3 && side1 + side3 > side2 &&
        side2 + side3 > side1) {
      possible_count += 1;
    }
  }

  std::cout << possible_count << std::endl;

  // part 2
  possible_count = 0;

  // reset to beginning of file
  f.clear();
  f.seekg(0);

  std::vector<std::vector<int> > sides;

  while (f >> side1 >> side2 >> side3) {
    sides.push_back({side1, side2, side3});
  }

  for (size_t i = 0; i < sides.size(); i += 3) {
    for (size_t j = 0; j < 3; j++) {
      if (sides[i][j] + sides[i + 1][j] > sides[i + 2][j] &&
          sides[i][j] + sides[i + 2][j] > sides[i + 1][j] &&
          sides[i + 1][j] + sides[i + 2][j] > sides[i][j]) {
        possible_count += 1;
      }
    }
  }

  std::cout << possible_count << std::endl;

  return 0;
}
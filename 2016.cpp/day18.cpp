#include "utils.h"

bool judge_tile(std::string above) {
  // judge whether a tile is safe or is a trap
  // based on the three tiles above
  // if trap, return true, vice versa
  assert(above.length() == 3);

  if (above[0] == '^') {
    // left tile is a trap
    if (above[1] == '^') {
      // center is also trap
      // is trap if right is not trap
      return above[2] != '^';
    } else {
      // center is not trap
      // is trap if right is not trap
      return above[2] != '^';
    }
  } else {
    // left is not trap
    if (above[1] == '^') {
      // center is trap
      // is trap if right is also trap
      return above[2] == '^';
    } else {
      // center is not trap
      // is trap if right is trap
      return above[2] == '^';
    }
  }
}

std::string next_row(std::string this_row) {
  std::string ret;
  size_t length = this_row.length();

  for (size_t i = 0; i < length; i++) {
    if (i == 0) {
      if (this_row[1] == '^') {
        // leftmost tile is a trap
        // whenever the second tile is a trap
        ret += "^";
      } else {
        ret += ".";
      }
    } else if (i == length - 1) {
      // rightmost tile is a trap
      // whenever the second last tile is a trap
      if (this_row[length - 2] == '^') {
        ret += "^";
      } else {
        ret += ".";
      }
    } else {
      // call helper function for non-special cases
      if (judge_tile(this_row.substr(i - 1, 3))) {
        ret += "^";
      } else {
        ret += ".";
      }
    }
  }

  return ret;
}

int main() {
  std::ifstream f("input18.txt");
  std::string row;
  f >> row;
  int total_safe = 0;

  for (size_t i = 0; i < 400000; i++) {
    total_safe += std::count(row.begin(), row.end(), '.');
    row = next_row(row);
  }

  std::cout << total_safe << std::endl;

  return 0;
}
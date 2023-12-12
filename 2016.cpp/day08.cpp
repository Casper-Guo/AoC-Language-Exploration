#include "utils.h"

int NUM_ROW = 6;
int NUM_COL = 50;

void rect(int a, int b, std::vector<std::vector<char> >& screen) {
  for (size_t row = 0; row < b; row++) {
    for (size_t col = 0; col < a; col++) {
      screen[row][col] = '#';
    }
  }
}

void rotate(bool row, int index, int shift,
            std::vector<std::vector<char> >& screen) {
  std::vector<char> temp;

  if (row) {
    temp.resize(NUM_COL);
    for (size_t i = 0; i < NUM_COL; i++) {
      temp[(i + shift) % NUM_COL] = screen[index][i];
    }
    screen[index] = temp;
  } else {
    temp.resize(NUM_ROW);
    for (size_t i = 0; i < NUM_ROW; i++) {
      temp[(i + shift) % NUM_ROW] = screen[i][index];
    }
    for (size_t i = 0; i < NUM_ROW; i++) {
      screen[i][index] = temp[i];
    }
  }
}

int main() {
  std::ifstream f("input08.txt");
  std::vector<std::string> lines = readlines(f);
  std::vector<std::vector<char> > screen(NUM_ROW,
                                         std::vector<char>(NUM_COL, '.'));

  std::vector<std::vector<std::string> > tokens;

  for (auto line : lines) {
    tokens.push_back(split(line));
  }

  // part 1
  for (auto operation : tokens) {
    int arg1, arg2;
    if (operation[0] == "rect") {
      arg1 = std::stoi(operation[1].substr(0, operation[1].find('x')));
      arg2 = std::stoi(operation[1].substr(operation[1].find('x') + 1));
      rect(arg1, arg2, screen);
    } else {
      // rotate
      arg1 = std::stoi(operation[2].substr(operation[2].find('=') + 1));
      arg2 = std::stoi(operation[4]);

      rotate(operation[1] == "row", arg1, arg2, screen);
    }
  }

  int num_lit = 0;

  for (size_t i = 0; i < NUM_ROW; i++) {
    for (size_t j = 0; j < NUM_COL; j++) {
      if (screen[i][j] == '#') {
        num_lit++;
      }
    }
  }

  std::cout << num_lit << std::endl;

  // part 2
  print_matrix(screen);

  return 0;
}
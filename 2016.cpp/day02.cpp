#include "utils.h"

int main() {
  std::ifstream f("input02.txt");
  std::string input_line;
  int button = 5;

  // part 1
  // while (std::getline(f, input_line)) {
  //   for (auto &ch : input_line) {
  //     switch (ch) {
  //       case 'U':
  //         if (button > 3) {
  //           button -= 3;
  //         }
  //         break;
  //       case 'D':
  //         if (button < 7) {
  //           button += 3;
  //         }
  //         break;
  //       case 'L':
  //         if (button % 3 != 1) {
  //           button -= 1;
  //         }
  //         break;
  //       case 'R':
  //         if (button % 3 != 0) {
  //           button += 1;
  //         }
  //         break;
  //     }
  //   }
  //   std::cout << button << std::endl;
  // }

  // part 2
  std::vector<std::vector<char> > pinpad = {{'\0', '\0', '1', '\0', '\0'},
                                            {'\0', '2', '3', '4', '\0'},
                                            {'5', '6', '7', '8', '9'},
                                            {'\0', 'A', 'B', 'C', '\0'},
                                            {'\0', '\0', 'D', '\0', '\0'}};

  // this pinpad is upside down right now
  std::reverse(pinpad.begin(), pinpad.end());

  int x = 0;
  int y = 2;

  while (std::getline(f, input_line)) {
    for (auto &ch : input_line) {
      switch (ch) {
        case 'U':
          if (y < 4 && pinpad[y + 1][x] != '\0') {
            y += 1;
          }
          break;
        case 'D':
          if (y > 0 && pinpad[y - 1][x] != '\0') {
            y -= 1;
          }
          break;
        case 'L':
          if (x > 0 && pinpad[y][x - 1] != '\0') {
            x -= 1;
          }
          break;
        case 'R':
          if (x < 4 && pinpad[y][x + 1] != '\0') {
            x += 1;
          }
          break;
      }
    }
    std::cout << pinpad[y][x] << std::endl;
  }

  return 0;
}
#include "utils.h"

std::string rotate_left(int x, std::string s) {
  s = s.substr(x) + s.substr(0, x);
  return s;
}

std::string rotate_right(int x, std::string s) {
  s = s.substr(s.length() - x) + s.substr(0, s.length() - x);
  return s;
}

std::string execute(std::string step, std::string password) {
  std::vector<std::string> tokens = split(step);

  if (tokens[0] == "swap") {
    // no changes needed for reversing
    if (is_int(tokens[1])) {
      int x = std::stoi(tokens[1]);
      int y = std::stoi(tokens[2]);

      std::swap(password[x], password[y]);
    } else {
      int x = password.find(tokens[1]);
      int y = password.find(tokens[2]);

      std::swap(password[x], password[y]);
    }
  } else if (tokens[0] == "rotate") {
    if (tokens[1] == "left") {
      int x = std::stoi(tokens[2]) % password.length();
      // part 1
      // password = rotate_left(x, password);
      // part 2
      password = rotate_right(x, password);
    } else if (tokens[1] == "right") {
      int x = std::stoi(tokens[2]) % password.length();
      // part 1
      // password = rotate_right(x, password);
      // part 2
      password = rotate_left(x, password);
    } else {
      // part 1
      // int x = 1 + password.find(tokens[1]);

      // if (x >= 5) {
      //   x++;
      // }

      // x = x % password.length();
      // password = rotate_right(x, password);

      // part 2
      // there is a one-to-one correspondence between the starting index
      // and where the letter ends up
      // the lookup tables associates the current index with the number of steps
      // to rotate left by, assuming length 8 string
      std::map<int, int> lookup = {{0, 1}, {1, 1}, {2, 6}, {3, 2},
                                   {4, 7}, {5, 3}, {6, 0}, {7, 4}};
      int current = password.find(tokens[1]);
      password = rotate_left(lookup[current], password);
    }
  } else if (tokens[0] == "reverse") {
    // no changes needed for reversing
    int x = std::stoi(tokens[1]);
    int y = std::stoi(tokens[2]);
    std::string temp = string_slice(password, x, y + 1);
    std::reverse(temp.begin(), temp.end());
    password = password.substr(0, x) + temp + password.substr(y + 1);
  } else if (tokens[0] == "move") {
    // part 1
    // int x = std::stoi(tokens[1]);
    // int y = std::stoi(tokens[2]);

    // part 2
    int x = std::stoi(tokens[2]);
    int y = std::stoi(tokens[1]);
    std::string temp = password.substr(0, x) + password.substr(x + 1);
    password = temp.substr(0, y) + password.substr(x, 1) + temp.substr(y);
  }
  return password;
}

int main() {
  std::ifstream f("input21.txt");
  std::vector<std::string> steps = readlines(f);

  // part 1
  std::string password = "abcdefgh";

  // for (auto step : steps) {
  //   password = execute(step, password);
  //   std::cout << step << " " << password << std::endl;
  // }

  // std::cout << password << std::endl;

  // part 2
  std::string decrypt = "dbfgaehc";
  std::reverse(steps.begin(), steps.end());

  for (auto step : steps) {
    decrypt = execute(step, decrypt);
    std::cout << step << " " << decrypt << std::endl;
  }

  std::cout << decrypt << std::endl;

  return 0;
}
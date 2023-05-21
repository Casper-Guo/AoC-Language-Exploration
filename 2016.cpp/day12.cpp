#include "utils.h"

void execute(std::string line, int& next, std::map<char, int>& registers) {
  std::vector<std::string> tokens = split(line);
  if (tokens[0] == "cpy") {
    if (is_int(tokens[1])) {
      registers[tokens[2][0]] = std::stoi(tokens[1]);
    } else {
      registers[tokens[2][0]] = registers[tokens[1][0]];
    }
    next++;
  } else if (tokens[0] == "inc") {
    registers[tokens[1][0]]++;
    next++;
  } else if (tokens[0] == "dec") {
    registers[tokens[1][0]]--;
    next++;
  } else if (tokens[0] == "jnz") {
    bool test;
    if (is_int(tokens[1])) {
      test = std::stoi(tokens[1]) != 0;
    } else {
      test = registers[tokens[1][0]] != 0;
    }

    if (test) {
      next += std::stoi(tokens[2]);
    } else {
      next++;
    }
  }
}

int main() {
  std::map<char, int> registers = {{'a', 0}, {'b', 0}, {'c', 1}, {'d', 0}};

  std::ifstream f("input12.txt");
  std::vector<std::string> lines = readlines(f);

  int next;

  while (next < lines.size()) {
    execute(lines[next], next, registers);
  }

  std::cout << registers['a'] << std::endl;

  return 0;
}
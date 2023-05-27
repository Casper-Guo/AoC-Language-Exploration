#include "utils.h"

int extract_value(std::string x, std::map<char, int>& registers) {
  // if x is an integer, return x
  // else, return the value stored in that register
  if (is_int(x)) {
    return std::stoi(x);
  } else {
    return registers[x[0]];
  }
}

void execute(std::string line, int& next, std::map<char, int>& registers) {
  std::vector<std::string> tokens = split(line);
  if (tokens[0] == "cpy") {
    registers[tokens[2][0]] = extract_value(tokens[1], registers);
    next++;
  } else if (tokens[0] == "inc") {
    registers[tokens[1][0]]++;
    next++;
  } else if (tokens[0] == "dec") {
    registers[tokens[1][0]]--;
    next++;
  } else if (tokens[0] == "jnz") {
    bool test = extract_value(tokens[1], registers) != 0;

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
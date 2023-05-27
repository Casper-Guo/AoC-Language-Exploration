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

void toggle_instruction(std::vector<std::string>& lines, int toggle) {
  if (toggle < 0 || toggle >= lines.size()) {
    return;
  }

  std::vector<std::string> tokens = split(lines[toggle]);

  if (tokens[0] == "non") {
    return;
  }

  if (tokens.size() == 2) {
    if (tokens[0] == "inc") {
      tokens[0] = "dec";
    } else {
      tokens[0] = "inc";
    }
  } else {
    if (tokens[0] == "jnz") {
      tokens[0] = "cpy";
    } else {
      tokens[0] = "jnz";
    }
  }

  lines[toggle] = join(tokens);
}

void execute(std::vector<std::string>& lines, int& next,
             std::map<char, int>& registers) {
  std::vector<std::string> tokens = split(lines[next]);
  if (tokens[0] == "cpy") {
    // deals with invalid cpy
    if (is_int(tokens[2])) {
      // trying to copy into something that's not a register
      return;
    }
    registers[tokens[2][0]] = extract_value(tokens[1], registers);
    next++;
  } else if (tokens[0] == "inc") {
    if (!is_int(tokens[1])) {
      registers[tokens[1][0]]++;
    }
    next++;
  } else if (tokens[0] == "dec") {
    if (!is_int(tokens[1])) {
      registers[tokens[1][0]]--;
    }
    next++;
  } else if (tokens[0] == "jnz") {
    bool test = extract_value(tokens[1], registers) != 0;

    if (test) {
      next += extract_value(tokens[2], registers);
    } else {
      next++;
    }
  } else if (tokens[0] == "tgl") {
    int toggle = next + extract_value(tokens[1], registers);
    toggle_instruction(lines, toggle);
    next++;
  } else if (tokens[0] == "mul") {
    int second = extract_value(tokens[3], registers);
    registers[tokens[1][0]] += abs(registers[tokens[2][0]]) * second;
    next++;
  } else {
    // non
    next++;
  }
}

int main() {
  std::map<char, int> registers = {{'a', 7}, {'b', 0}, {'c', 0}, {'d', 0}};

  std::ifstream f("input23.txt");
  std::vector<std::string> lines = readlines(f);

  int next = 0;

  while (next < lines.size()) {
    execute(lines, next, registers);
  }

  std::cout << registers['a'] << std::endl;

  return 0;
}
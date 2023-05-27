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
             std::map<char, int>& registers, int& signal) {
  std::vector<std::string> tokens = split(lines[next]);
  if (tokens[0] == "cpy") {
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
      if (extract_value(tokens[2], registers) <= next) {
        next += extract_value(tokens[2], registers);
      }
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
  } else if (tokens[0] == "out") {
    signal = extract_value(tokens[1], registers);
    std::cout << signal;
    next++;
  } else {
    // non
    next++;
  }
}

int main() {
  std::map<char, int> registers = {{'a', 100}, {'b', 0}, {'c', 0}, {'d', 0}};

  std::ifstream f("input25.txt");
  std::vector<std::string> lines = readlines(f);

  int next = 0;
  int num_iter = 0;
  int last_signal = 0;
  int signal = 1;
  int iter_limit = 20000;

  for (size_t i = 1; i < 1000; i++) {
    registers['a'] = i;
    registers['b'] = 0;
    registers['c'] = 0;
    registers['d'] = 0;

    std::cout << "\nTesting a = " << i << std::endl;
    while (next < lines.size() && num_iter++ < iter_limit) {
      execute(lines, next, registers, signal);
      if (signal < 0 || signal > 1) {
        break;
      }
      last_signal = signal;

      if (next == 27) {
        iter_limit += 10000;
      }
      if (num_iter > 100000) {
        break;
      }
    }
    next = 0;
    num_iter = 0;
    iter_limit = 100000;
    last_signal = 1;
    signal = 0;
  }

  return 0;
}
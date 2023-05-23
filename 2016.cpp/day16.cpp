#include "utils.h"

std::string generate(std::string a) {
  std::string b = a;
  std::reverse(b.begin(), b.end());

  for (char &i : b) {
    if (i == '0') {
      i = '1';
    } else if (i == '1') {
      i = '0';
    }
  }

  return a + "0" + b;
}

std::string checksum(std::string s) {
  std::string ret;

  for (size_t i = 1; i < s.length(); i += 2) {
    if (s[i] == s[i - 1]) {
      ret += "1";
    } else {
      ret += "0";
    }
  }

  return ret;
}

int main() {
  std::string input = "11101000110010100";
  size_t disk_size = 35651584;

  while (input.length() < disk_size) {
    input = generate(input);
  }

  std::string check = checksum(string_slice(input, 0, int(disk_size)));
  while (check.length() % 2 == 0) {
    check = checksum(check);
  }

  std::cout << check << std::endl;
  return 0;
}
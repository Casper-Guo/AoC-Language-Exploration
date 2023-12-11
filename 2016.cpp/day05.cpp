#include "utils.h"

bool filled(std::string password) {
  for (auto i : password) {
    if (i == ' ') {
      return false;
    }
  }
  return true;
}

int main() {
  // part 1
  std::string input = "reyedfim";
  std::string password, hash;
  int salt = 0;

  while (password.size() < 8) {
    hash = md5(input + std::to_string(salt));
    if (hash.substr(0, 5) == "00000") {
      password.push_back(hash[5]);
    }
    salt++;
  }

  std::cout << password << std::endl;

  // part 2
  password = std::string(8, ' ');
  salt = 0;
  while (!filled(password)) {
    hash = md5(input + std::to_string(salt));
    if (hash.substr(0, 5) == "00000") {
      if (isdigit(hash[5])) {
        int pos = hash[5] - '0';
        if (pos <= 7 && password[pos] == ' ') {
          password[pos] = hash[6];
        }
      }
    }
    salt++;
  }

  std::cout << password << std::endl;

  return 0;
}
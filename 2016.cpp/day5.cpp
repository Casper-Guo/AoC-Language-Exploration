#include <openssl/md5.h>

#include "utils.h"

std::string md5(const std::string &str) {
  unsigned char hash[MD5_DIGEST_LENGTH];

  MD5_CTX md5;
  MD5_Init(&md5);
  MD5_Update(&md5, str.c_str(), str.size());
  MD5_Final(hash, &md5);

  std::stringstream ss;

  for (int i = 0; i < MD5_DIGEST_LENGTH; i++) {
    ss << std::hex << std::setw(2) << std::setfill('0')
       << static_cast<int>(hash[i]);
  }
  return ss.str();
}

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
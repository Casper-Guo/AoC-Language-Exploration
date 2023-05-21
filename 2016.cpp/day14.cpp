#include "utils.h"

char find_triple(std::string s) {
  for (size_t i = 1; i < s.length() - 1; i++) {
    if (s[i] == s[i - 1] && s[i] == s[i + 1]) {
      return s[i];
    }
  }
  return '\0';
}

std::string key_stretching(std::string s) {
  std::string hash = s;

  for (size_t i = 0; i < 2017; i++) {
    hash = md5(hash);
  }

  return hash;
}

int main() {
  int index = 0;
  std::string salt = "ahsbgdzn";
  std::string raw, hash, quintuple;
  std::map<int, char> potential_keys;
  std::set<int> confirmed_keys;

  while (index < INT_MAX && confirmed_keys.size() <= 64) {
    raw = salt + std::to_string(index);

    // part 1
    // hash = md5(raw);

    // part 2
    hash = key_stretching(raw);

    char key = find_triple(hash);

    if (key != '\0') {
      potential_keys[index] = key;
    }

    for (auto i : potential_keys) {
      quintuple = std::string(5, i.second);
      if (hash.find(quintuple) != std::string::npos) {
        if (i.first != index) {
          confirmed_keys.insert(i.first);
        }
      }
    }

    std::erase_if(potential_keys, [index, confirmed_keys](auto& i) {
      return index - i.first > 1000 ||
             confirmed_keys.find(i.first) != confirmed_keys.end();
    });
    index++;
  }

  std::cout << confirmed_keys << std::endl
            << confirmed_keys.size() << std::endl;

  return 0;
}
#include "utils.h"

std::vector<std::string> split(std::string s, char delimiter) {
  std::vector<std::string> splits;
  std::stringstream ss(s);
  std::string word;

  while (!ss.eof()) {
    std::getline(ss, word, delimiter);
    splits.push_back(word);
  }

  return splits;
}
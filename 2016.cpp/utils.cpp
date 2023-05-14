#include "utils.h"

std::vector<std::string> split(std::string s, char delimiter = ' ') {
  std::vector<std::string> splits;
  std::stringstream ss(s);
  std::string word;

  while (!ss.eof()) {
    std::getline(ss, word, delimiter);
    splits.push_back(word);
  }

  return splits;
}

std::vector<std::string> split_csv(std::string s) {
  // assuming the following format
  // <item1>, <item2>, <item3>...
  std::vector<std::string> splits = split(s);
  for (size_t i = 0; i < splits.size(); ++i) {
    if (splits[i].find(',') != std::string::npos) {
      splits[i] = splits[i].substr(0, splits[i].length() - 1);
    }
  }

  return splits;
}

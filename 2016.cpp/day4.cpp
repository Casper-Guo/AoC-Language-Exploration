#include "utils.h"

std::vector<std::vector<std::string> > process(std::ifstream& f) {
  std::string line;
  std::vector<std::vector<std::string> > tokens;

  while (std::getline(f, line)) {
    tokens.push_back(split(line, '-'));
  }

  for (auto& line : tokens) {
    std::string last_token = line[line.size() - 1];
    size_t left_bracket = last_token.find('[');
    size_t right_bracket = last_token.find(']');

    line[line.size() - 1] = last_token.substr(0, left_bracket);
    line.push_back(
        last_token.substr(left_bracket + 1, right_bracket - left_bracket - 1));
  }

  return tokens;
}

bool sort_freq(std::pair<char, int> a, std::pair<char, int> b) {
  if (a.second != b.second) {
    return a.second > b.second;
  } else {
    return a.first < b.first;
  }
}

int main() {
  std::ifstream f("input4.txt");
  std::vector<std::vector<std::string> > tokens = process(f);

  // part 1
  int ID_sum = 0;

  for (auto& line : tokens) {
    std::map<char, int> freq;

    for (size_t token = 0; token < line.size() - 2; ++token) {
      for (char i : line[token]) {
        if (freq.find(i) != freq.end()) {
          freq[i] += 1;
        } else {
          freq[i] = 1;
        }
      }
    }

    std::vector<std::pair<char, int> > freq_items = items(freq);
    std::sort(freq_items.begin(), freq_items.end(), sort_freq);

    std::string checksum = line[line.size() - 1];
    bool real_room = false;
    for (size_t i = 0; i < checksum.length(); ++i) {
      real_room = checksum[i] == freq_items[i].first;
    }

    int id = std::stoi(line[line.size() - 2]);
    if (real_room) {
      ID_sum += id;
    }
  }

  std::cout << ID_sum << std::endl;

  return 0;
}
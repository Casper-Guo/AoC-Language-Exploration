#include "utils.h"

int main() {
  std::ifstream f("input6.txt");
  std::vector<std::string> lines = readlines(f);
  int num_rows = lines.size();
  int row_length = lines[0].length();

  std::vector<std::string> transpose(row_length);
  std::vector<std::pair<char, int> > freq;

  for (size_t i = 0; i < num_rows; i++) {
    for (size_t j = 0; j < row_length; j++) {
      transpose[j].push_back(lines[i][j]);
    }
  }

  for (auto line : transpose) {
    freq = items(char_freq(line));
    sort_items(freq);
    std::cout << freq[0].first;
  }

  std::cout << std::endl;

  // part 2 requires a slight modification to the sort_items function
  // lower values are higher priority

  return 0;
}
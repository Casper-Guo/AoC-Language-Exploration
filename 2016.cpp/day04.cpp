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

char shift_char(char original, int sector_ID) {
  return char('a' + ((original + sector_ID - 97) % 26));
}

std::string shift_string(std::string original, int sector_ID) {
  for (char& i : original) {
    i = shift_char(i, sector_ID);
  }
  return original;
}

int main() {
  std::ifstream f("input04.txt");
  std::vector<std::vector<std::string> > tokens = process(f);

  // part 1
  int ID_sum = 0;

  for (auto& line : tokens) {
    std::map<char, int> freq;

    for (size_t token = 0; token < line.size() - 2; ++token) {
      merge_map(freq, char_freq(line[token]));
    }

    std::vector<std::pair<char, int> > freq_items = items(freq);
    std::sort(freq_items.begin(), freq_items.end(), sort_freq);

    std::string checksum = line[line.size() - 1];
    bool real_room = true;
    for (size_t i = 0; i < checksum.length(); ++i) {
      if (checksum[i] != freq_items[i].first) {
        real_room = false;
      }
    }

    int id = std::stoi(line[line.size() - 2]);
    if (real_room) {
      ID_sum += id;
    }
  }

  std::cout << ID_sum << std::endl;

  // part 2
  std::vector<std::string> target = {"northpole", "object", "storage"};
  for (auto line : tokens) {
    int sector_id = std::stoi(line[line.size() - 2]);
    if (line.size() != 5) {
      continue;
    } else {
      std::vector<std::string> decrypted;
      for (size_t i = 0; i < 3; i++) {
        decrypted.push_back(shift_string(line[i], sector_id));
      }
      if (decrypted == target) {
        std::cout << sector_id << std::endl;
        break;
      }
    }
  }

  return 0;
}

#include "utils.h"

void get_arg(std::string args, int& length, int& rep) {
  std::vector<std::string> splits = split(args, 'x');

  length = std::stoi(splits[0]);
  rep = std::stoi(splits[1]);
}

int64_t calc_length(std::string s) {
  if (s.find('(') == std::string::npos) {
    return s.length();
  }

  size_t marker_start = s.find('(');
  size_t marker_end = s.find(')');

  int length, rep;

  get_arg(string_slice(s, marker_start + 1, marker_end), length, rep);
  std::string to_decompress = s.substr(marker_end + 1, length);
  std::string remaining = s.substr(marker_end + 1 + length);

  return marker_start + rep * calc_length(to_decompress) +
         calc_length(remaining);
}

int main() {
  std::ifstream f("input09.txt");
  std::string compressed;
  f >> compressed;
  std::stringstream decompressed;

  // part 1
  size_t left = 0;
  size_t right = 0;

  int length, rep;

  for (size_t i = 0; i < compressed.size(); ++i) {
    if (compressed[i] == '(') {
      left = i;

      // ...) {get this part} ( ...
      decompressed << string_slice(compressed, right, left);
    } else if (compressed[i] == ')') {
      right = i;
      get_arg(string_slice(compressed, left + 1, right), length, rep);

      // get length characters after )
      std::string repeat = compressed.substr(right + 1, length);

      for (size_t j = 0; j < rep; j++) {
        decompressed << repeat;
      }
      i += length;
      left = i + 1;
      right = i + 1;
    }
  }

  // ) {get this part}\0
  decompressed << compressed.substr(right);
  std::string final = decompressed.str();
  std::cout << final.length() << std::endl;

  // part 2
  std::cout << calc_length(compressed) << std::endl;

  return 0;
}
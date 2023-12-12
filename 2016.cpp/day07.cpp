#include "utils.h"

bool contains_abba(std::string s) {
  if (s.length() < 4) {
    return false;
  }

  std::string segment, reverse;
  for (size_t i = 0; i <= s.length() - 4; ++i) {
    segment = s.substr(i, 2);
    reverse = s.substr(i + 2, 2);
    std::reverse(reverse.begin(), reverse.end());
    if (reverse == segment && segment[0] != segment[1]) {
      return true;
    }
  }
  return false;
}

std::set<std::string> match_aba(std::string s) {
  std::set<std::string> matches;

  if (s.length() < 3) {
    return matches;
  }

  std::string segment;

  for (size_t i = 0; i <= s.length() - 3; ++i) {
    segment = s.substr(i, 3);
    if (segment[0] == segment[2] && segment[0] != segment[1]) {
      matches.insert(segment);
    }
  }
  return matches;
}

std::string aba_to_bab(std::string aba) {
  std::string bab;
  bab.push_back(aba[1]);
  bab.push_back(aba[0]);
  bab.push_back(aba[1]);
  return bab;
}

bool tls_support(std::string s) {
  size_t left = 0;
  size_t right = 0;
  size_t has_abba = false;

  for (size_t i = 0; i < s.size(); ++i) {
    if (s[i] == '[') {
      left = i;
      if (contains_abba(s.substr(right, left - right))) {
        has_abba = true;
      }
    } else if (s[i] == ']') {
      right = i;
      if (contains_abba(s.substr(left, right - left))) {
        return false;
      }
    }
  }
  if (contains_abba(s.substr(right))) {
    has_abba = true;
  }

  return has_abba;
}

bool ssl_support(std::string s) {
  size_t left = 0;
  size_t right = 0;
  std::set<std::string> abas, babs, temp;

  for (size_t i = 0; i < s.size(); ++i) {
    if (s[i] == '[') {
      left = i;
      temp = match_aba(s.substr(right, left - right));
      abas.insert(temp.begin(), temp.end());
    } else if (s[i] == ']') {
      right = i;
      temp = match_aba(s.substr(left, right - left));
      babs.insert(temp.begin(), temp.end());
    }
  }
  temp = match_aba(s.substr(right));
  abas.insert(temp.begin(), temp.end());

  for (auto i : abas) {
    if (babs.find(aba_to_bab(i)) != babs.end()) {
      return true;
    }
  }

  return false;
}

int main() {
  std::ifstream f("input07.txt");
  std::vector<std::string> lines = readlines(f);

  int support_tls = 0;
  int support_ssl = 0;
  for (auto line : lines) {
    if (tls_support(line)) {
      support_tls++;
    }
    if (ssl_support(line)) {
      support_ssl++;
    }
  }

  std::cout << support_tls << " " << support_ssl << std::endl;
  return 0;
}
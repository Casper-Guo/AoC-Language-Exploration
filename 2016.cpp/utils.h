#ifndef UTILS_H
#define UTILS_H

#include <limits.h>
#include <openssl/md5.h>
#include <stdint.h>

#include <algorithm>
#include <cassert>
#include <cmath>
#include <deque>
#include <exception>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <iterator>
#include <map>
#include <random>
#include <regex>
#include <set>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

std::vector<std::string> split(std::string s, char delimiter = ' ');
std::vector<std::string> split_csv(std::string s);
std::map<char, int> char_freq(std::string s);
std::vector<std::string> readlines(std::ifstream& f);
bool is_int(const std::string& s);
std::string md5(const std::string& str);

template <typename T>
std::string string_slice(std::string s, T left, T right) {
  // left is inclusive, right is exclusive
  return s.substr(left, right - left);
}

template <typename T>
std::ostream& operator<<(std::ostream& os, const std::set<T>& s) {
  for (auto i : s) {
    os << i << " ";
  }
  os << std::endl;

  return os;
}

template <typename T>
std::ostream& operator<<(std::ostream& os, const std::vector<T>& vec) {
  for (auto i : vec) {
    os << i << " ";
  }
  os << std::endl;

  return os;
}

template <typename T>
std::ostream& operator<<(std::ostream& os,
                         const std::vector<std::vector<T> >& vec) {
  for (auto row : vec) {
    os << row;
  }
  return os;
}

template <typename T1, typename T2>
std::ostream& operator<<(std::ostream& os, const std::pair<T1, T2>& pair) {
  os << pair.first << " " << pair.second << " " << std::endl;
  return os;
}

template <typename T1, typename T2>
std::ostream& operator<<(std::ostream& os, const std::map<T1, T2>& m) {
  for (auto i : m) {
    os << i.first << ": " << i.second << std::endl;
  }
  return os;
}

template <typename T>
std::ostream& operator<<(std::ostream& os, const std::deque<T>& d) {
  for (auto i : d) {
    os << i << " ";
  }
  os << std::endl;

  return os;
}

template <typename T>
std::vector<std::vector<T> > matrix_transpose(const std::vector<T>& vec) {
  int dim1 = vec.size();
  int dim2 = vec[0].size();
  std::vector<std::vector<T> > transpose(dim2, std::vector<T>(dim1));

  for (size_t i = 0; i < dim1; i++) {
    if (vec[i].size() != dim2) {
      throw std::range_error("Input matrix has inconsistent row lengths.");
    }
    for (size_t j = 0; j < dim2; j++) {
      transpose[j][i] = vec[i][j];
    }
  }

  return transpose;
}

template <typename T1, typename T2>
std::vector<T1> keys(const std::map<T1, T2>& map) {
  std::vector<T1> keys;
  for (auto it = map.begin(); it != map.end(); it++) {
    keys.push_back(it->first);
  }

  return keys;
}

template <typename T1, typename T2>
std::vector<T2> values(const std::map<T1, T2>& map) {
  std::vector<T2> values;
  for (auto it = map.begin(); it != map.end(); it++) {
    values.push_back(it->second);
  }

  return values;
}

template <typename T1, typename T2>
std::vector<std::pair<T1, T2> > items(const std::map<T1, T2>& map) {
  std::vector<std::pair<T1, T2> > items;
  for (auto it = map.begin(); it != map.end(); it++) {
    items.push_back({it->first, it->second});
  }

  return items;
}

template <typename T1, typename T2>
void merge_map(std::map<T1, T2>& map1, const std::map<T1, T2>& map2) {
  // merge map2 into map1, map1 is modified
  // if a key in map2 is present in map1, the values are added
  // else, the key is added to map1
  for (auto i : map2) {
    if (map1.find(i.first) != map1.end()) {
      map1[i.first] += i.second;
    } else {
      map1[i.first] = i.second;
    }
  }
}

template <typename T1, typename T2>
std::vector<std::pair<T1, T2> > sort_items(
    std::vector<std::pair<T1, T2> >& items, bool reverse = false) {
  // sort map items by value descending
  // ties broken by key (ascending)
  // if reverse=true, the values are sorted ascending

  std::sort(
      items.begin(), items.end(),
      [](const std::pair<T1, T2>& lhs, const std::pair<T1, T2>& rhs) -> bool {
        return lhs.first < rhs.first;
      });
  std::sort(items.begin(), items.end(),
            [reverse](const std::pair<T1, T2>& lhs,
                      const std::pair<T1, T2>& rhs) -> bool {
              if (reverse) {
                return lhs.second > rhs.second;
              } else {
                return lhs.second < rhs.second;
              }
            });

  return items;
}

#endif
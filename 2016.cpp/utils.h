#ifndef UTILS_H
#define UTILS_H

#include <algorithm>
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

std::vector<std::string> split(const std::string s, const char delimiter);
std::vector<std::string> split_csv(const std::string s);
std::map<char, int> char_freq(const std::string s);
std::vector<std::string> readlines(std::ifstream& f);

template <typename T>
void print_vector(const std::vector<T>& vec) {
  for (auto it = vec.begin(); it != vec.end(); ++it) {
    std::cout << *it << " ";
  }
  std::cout << std::endl;
}

template <typename T>
void print_matrix(const std::vector<std::vector<T> >& vec) {
  for (auto row : vec) {
    print(row);
  }
}

template <typename T1, typename T2>
void print_pairs(const std::vector<std::pair<T1, T2> >& vec) {
  for (auto pair : vec) {
    std::cout << pair.first << " " << pair.second << " ";
  }
  std::cout << std::endl;
}

template <typename T>
std::vector<T> vector_slice(const std::vector<T>& vec, int start, int end) {
  auto start_iter = vec.begin() + start;
  auto end_iter = vec.begin() + end - 1;
  std::vector<T> result;
  std::copy(start_iter, end_iter, result);

  return result;
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
    std::vector<std::pair<T1, T2> >& items) {
  // sort map items by value
  // ties broken by key

  std::sort(
      items.begin(), items.end(),
      [](const std::pair<T1, T2>& lhs, const std::pair<T1, T2>& rhs) -> bool {
        return lhs.first < rhs.first;
      });
  std::sort(
      items.begin(), items.end(),
      [](const std::pair<T1, T2>& lhs, const std::pair<T1, T2>& rhs) -> bool {
        return lhs.second < rhs.second;
      });

  return items;
}

#endif
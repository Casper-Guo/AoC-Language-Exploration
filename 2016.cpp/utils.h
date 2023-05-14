#ifndef UTILS_H
#define UTILS_H

#include <algorithm>
#include <cmath>
#include <deque>
#include <fstream>
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

std::vector<std::string> split(std::string s, char delimiter);
std::vector<std::string> split_csv(std::string s);

template <typename T>
void print(const std::vector<T>& vec) {
  for (auto it = vec.begin(); it != vec.end(); ++it) {
    std::cout << *it << " ";
  }
  std::cout << std::endl;
}

template <typename T>
void print_2d(const std::vector<std::vector<T> >& vec) {
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

#endif
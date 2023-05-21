#include "utils.h"
typedef std::pair<int, int> Config;

// need to find x such that
// for all (i, j) in configs
// (j + x) % i == 0
// Can we do better than brute force?
// Looks like brute force isn't so bad
// Wonder what the time complexity is in terms of
// the number of disks

bool validate_time(int time, const std::vector<Config>& configs) {
  int num_position, initial;
  for (size_t i = 0; i < configs.size(); i++) {
    num_position = configs[i].first;
    initial = configs[i].second;

    if ((initial + time + i + 1) % num_position != 0) {
      return false;
    }
  }
  return true;
}

int main() {
  std::vector<Config> configs{{13, 10}, {17, 15}, {19, 17}, {7, 1},
                              {5, 0},   {3, 1},   {11, 0}};

  int time = 0;

  while (time < INT_MAX) {
    if (validate_time(time, configs)) {
      std::cout << time << std::endl;
      break;
    }
    time++;
  }

  return 0;
}
#include "utils.h"

int steal_from(size_t num_elves, int index) {
  return (index + num_elves / 2) % num_elves;
}

int main() {
  int num_elves = 3001330;

  // part 1
  // std::vector<std::pair<int, int> > elves, temp;

  // for (size_t i = 0; i < num_elves; i++) {
  //   elves.push_back(std::make_pair(i + 1, 1));
  // }

  // while (elves.size() > 1) {
  // for (size_t i = 0; i < num_elves - 1; i++) {
  //   if (elves[i].second == 0) {
  //     continue;
  //   }

  //   elves[i].second += elves[i + 1].second;
  //   elves[i + 1].second = 0;
  // }

  // special logic for the last elf
  // as he has to wrap around
  // if (elves[elves.size() - 1].second != 0) {
  //   elves[elves.size() - 1].second += elves[0].second;
  //   elves[0].second = 0;
  // }

  // std::copy_if(elves.begin(), elves.end(), std::back_inserter(temp),
  //              [](auto i) { return i.second != 0; });
  // elves = temp;
  // temp.clear();

  // std::cout << elves[0].first << std::endl;

  // part 2
  std::deque<int> left, right;

  for (size_t i = 1; i < num_elves / 2 + 1; i++) {
    left.push_back(i);
  }

  for (size_t i = num_elves / 2 + 1; i <= num_elves; i++) {
    right.push_front(i);
  }

  while (!(left.empty() || right.empty())) {
    if (left.size() > right.size()) {
      left.pop_back();
    } else {
      right.pop_back();
    }

    right.push_front(left.front());
    left.pop_front();
    left.push_back(right.back());
    right.pop_back();
  }

  std::cout << left.front() << std::endl;

  return 0;
}
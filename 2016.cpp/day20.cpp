#include "utils.h"
typedef std::pair<long long, long long> Interval;

Interval process_line(std::string line) {
  size_t split = line.find('-');
  long long start = std::strtol(line.substr(0, split).c_str(), nullptr, 10);
  long long end = std::strtol(line.substr(split + 1).c_str(), nullptr, 10);

  return std::make_pair(start, end);
}

int main() {
  std::ifstream f("input20.txt");
  std::vector<std::string> lines = readlines(f);
  std::vector<Interval> intervals;

  for (auto line : lines) {
    intervals.push_back(process_line(line));
  }

  std::sort(intervals.begin(), intervals.end());

  long long max_ip = 4294967295;
  long long start = intervals[0].first;
  long long end = intervals[0].second;
  long long unblocked = 4294967295;
  long long num_allowed = 0;
  size_t i = 1;

  if (start != 0) {
    num_allowed = start;
  }

  while (i < intervals.size()) {
    if (intervals[i].first <= end) {
      // partial overlap with the previous interval
      end = std::max(end, intervals[i].second);
    } else {
      // no overlap with the previous interval

      // part 1
      // unblocked = end + 1;
      // break;

      // part 2
      start = intervals[i].first;
      num_allowed += (start - end - 1);
      end = intervals[i].second;
    }
    i++;
  }

  num_allowed += (max_ip - end);

  std::cout << num_allowed << std::endl;

  return 0;
}
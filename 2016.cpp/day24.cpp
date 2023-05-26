#include "utils.h"
typedef std::pair<int, int> Location;
typedef std::map<int, std::map<int, int> > Distance;
typedef std::pair<std::pair<int, int>, int> Steps;

int count_steps(const std::vector<int>& path, Distance& dist) {
  int steps = 0;

  for (size_t i = 0; i < path.size() - 1; i++) {
    steps += dist[path[i]][path[i + 1]];
  }

  return steps;
}

std::vector<Location> valid_moves(const Location& current,
                                  const std::vector<std::string>& grid) {
  int x = current.first;
  int y = current.second;
  assert(grid[y][x] != '#');

  std::vector<Location> valid_moves;

  if (x - 1 > 0 && grid[y][x - 1] != '#') {
    valid_moves.push_back({x - 1, y});
  }

  if (x + 1 < grid[0].size() && grid[y][x + 1] != '#') {
    valid_moves.push_back({x + 1, y});
  }

  if (y - 1 > 0 && grid[y - 1][x] != '#') {
    valid_moves.push_back({x, y - 1});
  }

  if (y + 1 < grid.size() && grid[y + 1][x] != '#') {
    valid_moves.push_back({x, y + 1});
  }
  return valid_moves;
}

int main() {
  std::ifstream f("input24.txt");
  std::vector<std::string> grid = readlines(f);
  int dest_count = 0;
  std::map<int, Location> destinations;
  Distance dist;

  // iterate through the grid once
  // find all the numbers
  for (size_t row = 0; row < grid.size(); row++) {
    for (size_t col = 0; col < grid[row].size(); col++) {
      if (std::isdigit(grid[row][col])) {
        dest_count++;
        destinations[grid[row][col] - '0'] = {col, row};
      }
    }
  }

  // initialize destination matrix
  for (size_t i = 0; i < dest_count; i++) {
    dist[i] = {{i, 0}};
  }

  // BFS
  std::deque<Steps> search_queue;
  std::set<Location> visited;

  for (size_t current_start = 0; current_start < dest_count; current_start++) {
    search_queue.push_back({destinations[current_start], 0});
    visited.insert(destinations[current_start]);

    while (dist[current_start].size() < dest_count) {
      assert(!search_queue.empty());
      Location current = search_queue.front().first;
      int current_steps = search_queue.front().second;
      search_queue.pop_front();

      if (std::isdigit(grid[current.second][current.first])) {
        int digit = grid[current.second][current.first] - '0';

        if (dist[current_start].find(digit) == dist[current_start].end()) {
          dist[current_start][digit] = current_steps;
          dist[digit][current_start] = current_steps;
        }
      }

      for (auto loc : valid_moves(current, grid)) {
        if (visited.find(loc) != visited.end()) {
          continue;
        }

        search_queue.push_back({loc, current_steps + 1});
        visited.insert(loc);
      }
    }
    visited.clear();
    search_queue.clear();
  }

  // optimize
  // I can Held-Karp this but it seems like a pain to implement in C++
  std::vector<int> paths(dest_count);
  std::iota(paths.begin(), paths.end(), 0);
  int min_steps = INT_MAX;

  // part 1
  while (std::next_permutation(paths.begin() + 1, paths.end())) {
    min_steps = std::min(min_steps, count_steps(paths, dist));
  }

  std::cout << min_steps << std::endl;

  // part 2
  min_steps = INT_MAX;
  paths.push_back(0);
  while (std::next_permutation(paths.begin() + 1, paths.end() - 1)) {
    min_steps = std::min(min_steps, count_steps(paths, dist));
  }

  std::cout << min_steps << std::endl;

  return 0;
}
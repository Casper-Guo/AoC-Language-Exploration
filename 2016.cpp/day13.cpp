#include "utils.h"
typedef std::pair<int, int> Grid;

bool validate_space(Grid grid) {
  int x = grid.first;
  int y = grid.second;
  if (x < 0 || y < 0) {
    return false;
  }

  int test = x * x + 3 * x + 2 * x * y + y + y * y;
  test += 1362;

  return __builtin_popcount(test) % 2 == 0;
}

std::vector<Grid> generate_moves(Grid grid) {
  std::vector<Grid> moves;
  int x = grid.first;
  int y = grid.second;

  if (validate_space({x + 1, y})) {
    moves.push_back({x + 1, y});
  }

  if (validate_space({x - 1, y})) {
    moves.push_back({x - 1, y});
  }

  if (validate_space({x, y + 1})) {
    moves.push_back({x, y + 1});
  }

  if (validate_space({x, y - 1})) {
    moves.push_back({x, y - 1});
  }

  return moves;
}

int main() {
  std::deque<Grid> search_queue;
  std::map<Grid, int> visited;
  Grid target{31, 39};
  visited[{1, 1}] = 0;
  search_queue.push_back({1, 1});

  while (!search_queue.empty()) {
    Grid current = search_queue.front();
    int current_moves = visited[current];
    search_queue.pop_front();

    // part 2
    if (current_moves == 50) {
      break;
    }

    for (auto i : generate_moves(current)) {
      if (visited.find(i) == visited.end()) {
        visited[i] = current_moves + 1;
        search_queue.push_back(i);
      }
    }

    // part 1
    // if (visited.find(target) != visited.end()) {
    //   std::cout << visited[target] << std::endl;
    //   break;
    // }
  }

  std::cout << visited.size() << std::endl;

  return 0;
}
#include "utils.h"
typedef std::pair<int, int> Grid;

std::vector<std::string> generate_moves(const std::string path,
                                        const Grid grid) {
  std::string password = "ioramepc";
  std::string hash = md5(password + path);
  std::string open = "bcdef";
  std::vector<std::string> valid_moves;

  if (open.find(hash[0]) != std::string::npos) {
    if (grid.second > 0) {
      valid_moves.push_back("U");
    }
  }

  if (open.find(hash[1]) != std::string::npos) {
    if (grid.second < 3) {
      valid_moves.push_back("D");
    }
  }

  if (open.find(hash[2]) != std::string::npos) {
    if (grid.first > 0) {
      valid_moves.push_back("L");
    }
  }

  if (open.find(hash[3]) != std::string::npos) {
    if (grid.first < 3) {
      valid_moves.push_back("R");
    }
  }

  return valid_moves;
}

Grid find_grid(const Grid current, const std::string move) {
  // Given the current grid and the next move
  // find the next grid
  int current_x = current.first;
  int current_y = current.second;

  if (move == "U") {
    return {current_x, current_y - 1};
  } else if (move == "D") {
    return {current_x, current_y + 1};
  } else if (move == "L") {
    return {current_x - 1, current_y};
  } else if (move == "R") {
    return {current_x + 1, current_y};
  }
  return {-1, -1};
}

int main() {
  std::map<std::string, Grid> visited;
  std::deque<std::string> bfs_queue;
  bfs_queue.push_back("");
  visited[""] = {0, 0};
  bool vault_reached;

  while (!bfs_queue.empty() && !vault_reached) {
    std::string current = bfs_queue.front();
    bfs_queue.pop_front();
    Grid current_grid = visited[current];
    int current_x = current_grid.first;
    int current_y = current_grid.second;

    for (std::string move : generate_moves(current, current_grid)) {
      std::string path = current + move;
      Grid next_grid = find_grid(current_grid, move);

      if (next_grid == std::make_pair(-1, -1)) {
        std::cerr << "Invalid move argument" << std::endl;
        exit(1);
      }

      if (next_grid == std::make_pair(3, 3)) {
        // part 1
        // std::cout << path << " " << path.length() << std::endl;
        // vault_reached = true;
        // break;

        // part 2
        // stop exploring this path
        visited[path] = next_grid;
        continue;
      }

      if (visited.find(path) == visited.end()) {
        bfs_queue.push_back(path);
        visited[path] = next_grid;
      }
    }
  }

  // part 1
  // if (!vault_reached) {
  //   std::cout << "No valid path to the vault." << std::endl;
  // }

  // part 2
  int max_moves = 0;

  for (auto i : visited) {
    if (i.second == std::make_pair(3, 3)) {
      if (i.first.length() > max_moves) {
        max_moves = i.first.length();
      }
    }
  }

  std::cout << max_moves << std::endl;

  return 0;
}
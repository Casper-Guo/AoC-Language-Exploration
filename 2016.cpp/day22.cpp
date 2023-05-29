#include "utils.h"
struct Node;
typedef std::pair<int, int> Coordinate;
typedef std::vector<std::vector<Node> > Grid;

struct Node {
  Coordinate coordinate;
  int used;
  int available;

  Node(int x, int y, int used, int available)
      : coordinate({x, y}), used(used), available(available) {}
};

std::ostream& operator<<(std::ostream& os, const Node& node) {
  os << "node-x" << node.coordinate.first << "-y" << node.coordinate.second;
  os << " Used: " << node.used << " Available: " << node.available << std::endl;
  return os;
}

Node node_factory(std::string line) {
  std::stringstream ss(line);
  std::string loc, size, used, available;
  ss >> loc >> size >> used >> available;

  // select x{}-y{}part
  loc = loc.substr(15, loc.find(" "));
  used = used.substr(0, used.find("T"));
  available = available.substr(0, available.find("T"));

  std::vector<std::string> coordinates = split(loc, '-');
  int x = std::stoi(coordinates[0].substr(1));
  int y = std::stoi(coordinates[1].substr(1));

  return Node{x, y, std::stoi(used), std::stoi(available)};
}

Node& get_node(const Coordinate& coordinate, Grid& grid) {
  return grid[coordinate.second][coordinate.first];
}

bool check_viable(const Coordinate& current, const Coordinate& next,
                  Grid& grid) {
  // check if it is possible to move data from current to next right now
  Node current_node = get_node(current, grid);
  Node next_node = get_node(next, grid);

  return next_node.available >= current_node.used;
}

bool worth_exploring(const Coordinate& current, const Coordinate& next,
                     Grid& grid) {
  // check if it is worth exploring further down this path
  // eventually we need to backtrack
  // so the current node's used must be smaller than next node's total
  Node current_node = get_node(current, grid);
  Node next_node = get_node(next, grid);

  return next_node.used + next_node.available >= current_node.used;
}

std::vector<Coordinate> generate_moves(const Coordinate& current, Grid& grid) {
  // generate all valid (inbound) moves from the present location
  // doesn't consider the relative data capacities
  std::vector<Coordinate> moves;
  if (current.first < grid[0].size() - 1) {
    moves.push_back({current.first + 1, current.second});
  }
  if (current.first > 0) {
    moves.push_back({current.first - 1, current.second});
  }

  if (current.second < grid.size() - 1) {
    moves.push_back({current.first, current.second + 1});
  }
  if (current.second > 0) {
    moves.push_back({current.first, current.second - 1});
  }

  return moves;
}

void move_data(const Coordinate& from, const Coordinate& to, Grid& grid) {
  // move all data in the from node to the to node
  // update node records
  Node& from_node = get_node(from, grid);
  Node& to_node = get_node(to, grid);

  assert(from_node.used <= to_node.available);

  from_node.available += from_node.used;
  to_node.available -= from_node.used;
  to_node.used += from_node.used;
  from_node.used = 0;
}

int backtrack(const Coordinate& end, const Coordinate& start,
              std::map<Coordinate, Coordinate>& path, Grid& grid) {
  // given a start and an end node and the path in between
  // backtrack, determine the number of steps taken
  int num_steps = 0;
  Coordinate current = end;

  while (current != start) {
    move_data(path[current], current, grid);
    current = path[current];
    num_steps += 1;
  }

  return num_steps;
}

int main() {
  std::ifstream f("input22.txt");
  std::vector<Node> nodes;
  std::vector<std::string> lines = readlines(f);
  lines.erase(lines.begin(), lines.begin() + 2);

  for (auto line : lines) {
    nodes.push_back(node_factory(line));
  }

  // part 1

  // Simple O(n ^ 2) implementation
  int num_viable = 0;
  for (size_t i = 0; i < nodes.size(); i++) {
    if (nodes[i].used == 0) {
      continue;
    }
    for (size_t j = 0; j < nodes.size(); j++) {
      if (i == j) {
        continue;
      }
      if (nodes[j].available >= nodes[i].used) {
        num_viable++;
      }
    }
  }

  std::cout << num_viable << std::endl;

  // O(nlogn) with two sorted vectors implementation
  // this will break part 2!
  // std::vector<Node> nodes_used = nodes;

  // // sort one vector by available ascending
  // std::sort(nodes.begin(), nodes.end(), [](const Node& a, const Node& b) {
  //   return a.available < b.available;
  // });
  // // sort the other by used ascending
  // std::sort(nodes_used.begin(), nodes_used.end(),
  //           [](const Node& a, const Node& b) { return a.used < b.used; });

  // size_t available_iter = 0;
  // size_t used_iter = 0;
  // num_viable = 0;

  // while (used_iter < nodes_used.size()) {
  //   if (nodes_used[used_iter].used != 0) {
  //     // move available iter to the first node that has enough space
  //     while (available_iter < nodes.size() &&
  //            nodes[available_iter].available < nodes_used[used_iter].used) {
  //       available_iter++;
  //     }

  //     num_viable += nodes.size() - available_iter;

  //     // minus one if the node itself has more space available than used
  //     if (nodes_used[used_iter].available >= nodes_used[used_iter].used) {
  //       num_viable--;
  //     }
  //   }
  //   used_iter++;
  // }

  // std::cout << num_viable << std::endl;

  // part 2
  // restructure 1D vector to 2D
  Grid grid;
  int num_rows = nodes[nodes.size() - 1].coordinate.second + 1;
  int num_cols = nodes[nodes.size() - 1].coordinate.first + 1;
  grid.resize(num_rows);

  for (size_t i = 0; i < nodes.size(); ++i) {
    grid[nodes[i].coordinate.second].push_back(nodes[i]);
  }

  Coordinate target_data{num_cols - 1, 0};

  // coordinate, prev pairs to enable BFS backtracking
  std::map<Coordinate, Coordinate> path;
  std::deque<Coordinate> search_queue;
  int num_steps = 0;
  Coordinate start_search;

  for (int i = num_cols - 2; i >= 0; i--) {
    // we want to move the data in target_data to start_search
    // so we need to move the data in start_search else where
    // and then swap
    bool end_search = false;
    start_search = grid[0][i].coordinate;
    search_queue.push_back(start_search);
    path[start_search] = start_search;

    while (!search_queue.empty() && !end_search) {
      Coordinate current = search_queue.front();
      search_queue.pop_front();

      std::vector<Coordinate> possible_moves = generate_moves(current, grid);

      for (auto move : possible_moves) {
        if (move == target_data) {
          // cannot move any other data into the target data
          continue;
        }
        if (check_viable(current, move, grid)) {
          // found a viable pair
          // terminate search and begin backtracking and moving immediately
          end_search = true;
          path[move] = current;
          num_steps += backtrack(move, start_search, path, grid);
          break;
        } else {
          if (worth_exploring(current, move, grid) &&
              path.find(move) == path.end()) {
            // not worth exploring example:
            // current: used = 28, available = 3
            // move: used = 5, next = 5
            // we can never backtrack along this path
            search_queue.push_back(move);
            path[move] = current;
          }
        }
      }
    }
    move_data(target_data, start_search, grid);
    target_data = start_search;
    num_steps += 1;
    search_queue.clear();
    path.clear();
  }

  std::cout << num_steps << std::endl;

  return 0;
}
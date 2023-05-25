#include "utils.h"

struct Node {
  int x;
  int y;
  int used;
  int available;

  Node(int x, int y, int used, int available)
      : x(x), y(y), used(used), available(available) {}
};

std::ostream& operator<<(std::ostream& os, const Node& node) {
  os << "node-x" << node.x << "-y" << node.y << std::endl;
  os << "Used: " << node.used << " Available: " << node.available << std::endl;
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

int main() {
  std::ifstream f("input22.txt");
  std::vector<Node> nodes;
  std::vector<std::string> lines = readlines(f);
  lines.erase(lines.begin(), lines.begin() + 2);

  for (auto line : lines) {
    nodes.push_back(node_factory(line));
  }

  // easy thing will be to do the O(n^2) nested loop
  // but is there a better way?

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
  std::vector<Node> nodes_used = nodes;

  // sort one vector by available ascending
  std::sort(nodes.begin(), nodes.end(), [](const Node& a, const Node& b) {
    return a.available < b.available;
  });
  // sort the other by used ascending
  std::sort(nodes_used.begin(), nodes_used.end(),
            [](const Node& a, const Node& b) { return a.used < b.used; });

  size_t available_iter = 0;
  size_t used_iter = 0;
  num_viable = 0;

  while (used_iter < nodes_used.size()) {
    if (nodes_used[used_iter].used != 0) {
      // move available iter to the first node that has enough space
      while (available_iter < nodes.size() &&
             nodes[available_iter].available < nodes_used[used_iter].used) {
        available_iter++;
      }

      num_viable += nodes.size() - available_iter;

      // minus one if the node itself has more space available than used
      if (nodes_used[used_iter].available >= nodes_used[used_iter].used) {
        num_viable--;
      }
    }
    used_iter++;
  }

  std::cout << num_viable << std::endl;

  return 0;
}
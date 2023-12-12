#include "utils.h"

enum class Direction { north, east, south, west };

void change_direction(Direction &direction, const char turn) {
  switch (direction) {
    case Direction::north:
      if (turn == 'R') {
        direction = Direction::east;
      } else if (turn == 'L') {
        direction = Direction::west;
      }
      break;

    case Direction::east:
      if (turn == 'R') {
        direction = Direction::south;
      } else if (turn == 'L') {
        direction = Direction::north;
      }
      break;

    case Direction::south:
      if (turn == 'R') {
        direction = Direction::west;
      } else if (turn == 'L') {
        direction = Direction::east;
      }
      break;

    case Direction::west:
      if (turn == 'R') {
        direction = Direction::north;
      } else if (turn == 'L') {
        direction = Direction::south;
      }
      break;
  }
}

void one_move(const Direction direction, const int steps, int &x, int &y) {
  switch (direction) {
    case Direction::north:
      y += steps;
      break;

    case Direction::east:
      x += steps;
      break;

    case Direction::south:
      y -= steps;
      break;

    case Direction::west:
      x -= steps;
      break;
  }
}

bool check_visited(const std::set<std::pair<int, int> > &visited, const int x,
                   const int y) {
  return visited.find(std::make_pair(x, y)) != visited.end();
}

int main() {
  std::ifstream f("input01.txt");
  std::string input;
  std::getline(f, input);
  std::vector<std::string> directions = split(input, ' ');

  Direction direction = Direction::north;
  int x = 0;
  int y = 0;
  bool found_hq = false;

  std::set<std::pair<int, int> > visited;

  for (std::string &step : directions) {
    if (step.find(',') != std::string::npos) {
      step = step.substr(0, step.size() - 1);
    }

    char turn = step[0];
    int steps = std::stoi(step.substr(1));

    int old_x = x;
    int old_y = y;

    change_direction(direction, turn);
    one_move(direction, steps, x, y);

    if (!found_hq) {
      switch (direction) {
        case Direction::north:
          for (int i = old_y + 1; i <= y; i++) {
            if (check_visited(visited, x, i)) {
              std::cout << abs(x) + abs(i) << std::endl;
              found_hq = true;
            } else {
              visited.insert(std::make_pair(x, i));
            }
          }
          break;

        case Direction::east:
          for (int i = old_x + 1; i <= x; i++) {
            if (check_visited(visited, i, y)) {
              std::cout << abs(i) + abs(y) << std::endl;
              found_hq = true;
            } else {
              visited.insert(std::make_pair(i, y));
            }
          }
          break;

        case Direction::south:
          for (int i = old_y - 1; i >= y; i--) {
            if (check_visited(visited, x, i)) {
              std::cout << abs(x) + abs(i) << std::endl;
              found_hq = true;
            } else {
              visited.insert(std::make_pair(x, i));
            }
          }
          break;

        case Direction::west:
          for (int i = old_x - 1; i >= x; i--) {
            if (check_visited(visited, i, y)) {
              std::cout << abs(i) + abs(y) << std::endl;
              found_hq = true;
            } else {
              visited.insert(std::make_pair(i, y));
            }
          }
          break;
      }
    }
  }

  std::cout << abs(x) + abs(y) << std::endl;

  return 0;
}
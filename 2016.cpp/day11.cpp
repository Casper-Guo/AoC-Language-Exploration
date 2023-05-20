#include "utils.h"
typedef std::vector<std::pair<int, int> > Location;
typedef std::pair<Location, int> State;

std::ostream& operator<<(std::ostream& os, State& state) {
  os << state.first;
  os << "Elevator at floor " << state.second << std::endl;

  return os;
}

bool validate_state(const State& state) {
  int chip_location, gen_location;
  Location location = state.first;

  if (state.second < 1 || state.second > 4) {
    return false;
  }

  for (size_t i = 0; i < location.size(); ++i) {
    chip_location = location[i].first;
    gen_location = location[i].second;

    if (!(chip_location >= 1 && chip_location <= 4)) {
      return false;
    }

    if (!(gen_location >= 1 && gen_location <= 4)) {
      return false;
    }
  }

  for (size_t i = 0; i < location.size(); ++i) {
    std::pair<int, int> current = location[i];

    if (current.first == current.second) {
      // chip on same floor with its generator
      // safe
      continue;
    } else {
      for (size_t j = 0; j < location.size(); ++j) {
        if (i == j) {
          continue;
        } else {
          // check against all other generator locations
          if (current.first == location[j].second) {
            return false;
          }
        }
      }
    }
  }
  return true;
}

std::set<State> generate_states(const State& state) {
  std::set<State> possible_states;
  State new_state = state;
  Location location = state.first;
  int elevator = state.second;

  // move one chip
  for (size_t i = 0; i < location.size(); ++i) {
    if (location[i].first == elevator) {
      new_state.first[i].first = location[i].first + 1;
      new_state.second = elevator + 1;
      possible_states.insert(new_state);

      new_state.first[i].first = location[i].first - 1;
      new_state.second = elevator - 1;
      possible_states.insert(new_state);

      new_state = state;
    }
  }

  // move one generator
  for (size_t i = 0; i < location.size(); ++i) {
    if (location[i].second == elevator) {
      new_state.first[i].second = location[i].second + 1;
      new_state.second = elevator + 1;
      possible_states.insert(new_state);

      new_state.first[i].second = location[i].second - 1;
      new_state.second = elevator - 1;
      possible_states.insert(new_state);

      new_state = state;
    }
  }

  // move two chips
  for (size_t i = 0; i < location.size(); ++i) {
    for (size_t j = 0; j < location.size(); ++j) {
      if (i == j) {
        continue;
      }

      if (location[i].first != location[j].first) {
        // not on the same floor
        continue;
      }

      if (location[i].first == elevator) {
        new_state.first[i].first = location[i].first + 1;
        new_state.first[j].first = location[j].first + 1;
        new_state.second = elevator + 1;
        possible_states.insert(new_state);

        new_state.first[i].first = location[i].first - 1;
        new_state.first[j].first = location[j].first - 1;
        new_state.second = elevator - 1;
        possible_states.insert(new_state);

        new_state = state;
      }
    }
  }

  // move two generators
  for (size_t i = 0; i < location.size(); ++i) {
    for (size_t j = 0; j < location.size(); ++j) {
      if (i == j) {
        continue;
      }

      if (location[i].second != location[j].second) {
        // not on the same floor
        continue;
      }

      if (location[i].second == elevator) {
        new_state.first[i].second = location[i].second + 1;
        new_state.first[j].second = location[j].second + 1;
        new_state.second = elevator + 1;
        possible_states.insert(new_state);

        new_state.first[i].second = location[i].second - 1;
        new_state.first[j].second = location[j].second - 1;
        new_state.second = elevator - 1;
        possible_states.insert(new_state);

        new_state = state;
      }
    }
  }

  // move a chip and a generator
  for (size_t i = 0; i < location.size(); i++) {
    if (location[i].first != location[i].second) {
      continue;
    }

    if (location[i].first == elevator) {
      new_state.first[i].first = location[i].first + 1;
      new_state.first[i].second = location[i].second + 1;
      new_state.second = elevator + 1;

      possible_states.insert(new_state);
      new_state.first[i].first = location[i].first - 1;
      new_state.first[i].second = location[i].second - 1;
      new_state.second = elevator - 1;
      possible_states.insert(new_state);

      new_state = state;
    }
  }

  std::set<State> valid_states;
  std::copy_if(possible_states.begin(), possible_states.end(),
               std::inserter(valid_states, valid_states.end()), validate_state);

  return valid_states;
}

int main() {
  // part 1 BFS
  // strontium, plutonium, thulium, ruthenium, curium, elerium, dilithium
  State initial{{{1, 1}, {1, 1}, {3, 2}, {2, 2}, {2, 2}, {1, 1}, {1, 1}}, 1};
  State target{{{4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 4}}, 4};

  std::set<State> visited;
  visited.insert(initial);

  std::deque<std::pair<State, int> > search_queue;
  search_queue.push_back({initial, 0});

  // std::map<State, State> graph;
  // graph[initial] = initial;

  while (!search_queue.empty()) {
    std::pair<State, int> current = search_queue.front();
    search_queue.pop_front();

    State current_state = current.first;
    int current_steps = current.second;

    if (current_state == target) {
      std::cout << current_steps << std::endl;
      break;
    }

    std::set<State> next_steps = generate_states(current_state);

    for (auto i : next_steps) {
      if (visited.find(i) == visited.end()) {
        search_queue.push_back({i, current_steps + 1});
        visited.insert(i);
        // graph[i] = current_state;
      }
    }
  }

  // output the path taken
  // std::vector<State> path;
  // State backtrack = target;

  // while (target != graph[target]) {
  //   path.push_back(graph[target]);
  //   target = graph[target];
  // }

  // for (size_t i = path.size() - 1; i > 0; i--) {
  //   std::cout << path[i];
  // }

  return 0;
}
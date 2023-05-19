#include "utils.h"

// Can assume there is no negative value chip in the input

struct Bot {
  int chip1 = -1;
  int chip2 = -1;
};

std::ostream &operator<<(std::ostream &os, Bot const &bot) {
  return os << bot.chip1 << " " << bot.chip2;
}

void pass_chip(int chip, Bot &bot) {
  if (bot.chip1 == -1) {
    bot.chip1 = chip;
  } else {
    bot.chip2 = chip;
  }
}

bool execute(const std::vector<std::string> &instruction,
             std::map<int, Bot> &bots, std::map<int, int> &outputs) {
  if (instruction.size() == 6) {
    int chip = std::stoi(instruction[1]);
    int bot_id = std::stoi(instruction[5]);

    if (bots.find(bot_id) == bots.end()) {
      bots[bot_id] = Bot{chip, -1};
    } else {
      pass_chip(chip, bots[bot_id]);
    }
  } else {
    int bot_id = std::stoi(instruction[1]);
    Bot bot = bots[bot_id];

    if (bot.chip1 == -1 || bot.chip2 == -1) {
      return false;
    }

    bool low_output = instruction[5] == "output";
    int low_target = std::stoi(instruction[6]);
    bool high_output = instruction[10] == "output";
    int high_target = std::stoi(instruction[11]);
    int low_chip = std::min(bot.chip1, bot.chip2);
    int high_chip = std::max(bot.chip1, bot.chip2);

    if (low_output) {
      outputs[low_target] = low_chip;
    } else {
      pass_chip(low_chip, bots[low_target]);
    }

    if (high_output) {
      outputs[high_target] = high_chip;
    } else {
      pass_chip(high_chip, bots[high_target]);
    }

    if (low_chip == 17 && high_chip == 61) {
      std::cout << bot_id << std::endl;
    }

    bot.chip1 = -1;
    bot.chip2 = -1;
  }

  return true;
}

int main() {
  std::ifstream f("input10.txt");
  std::vector<std::string> lines = readlines(f);
  std::set<std::vector<std::string> > instructions;
  std::map<int, Bot> bots;
  std::map<int, int> outputs;

  for (auto line : lines) {
    instructions.insert(split(line));
  }

  while (!instructions.empty()) {
    for (auto instruction : instructions) {
      if (execute(instruction, bots, outputs)) {
        instructions.erase(instruction);
        break;
      }
    }
  }

  std::cout << outputs[0] * outputs[1] * outputs[2] << std::endl;

  return 0;
}
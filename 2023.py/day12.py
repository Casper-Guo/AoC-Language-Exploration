import regex as re
from functools import cache
import utils


def process_line(line):
    line = line.split()

    # replace consecutive operational springs
    line[0] = re.sub(r"\.+", ".", line[0])

    return tuple([i for i in line[0]]), tuple(utils.ints(line[1]))


@cache
def calc_config(condition, groups, current_group=0):
    # base cases
    if not condition:
        if current_group:
            return int(len(groups) == 1 and current_group == groups[0])
        else:
            return int(len(groups) == 0)

    if current_group:
        # current group is too long
        if not groups or current_group > groups[0]:
            return 0

    if not groups:
        return int("#" not in condition)

    # recursive cases
    if condition[0] == ".":
        # if a group has started
        # then check whether it is the correct length
        # if yes, move onto the next group, or else terminates
        # If a group hasn't started, do nothing
        if current_group:
            if current_group != groups[0]:
                return 0
            else:
                groups = groups[1:]
        return calc_config(condition[1:], groups, 0)
    if condition[0] == "#":
        # increment current group length
        return calc_config(condition[1:], groups, current_group + 1)
    else:
        # this location can either be operational or broken
        if not groups or current_group == groups[0]:
            # if current group length matches the first group in groups
            # or that there are no remaining groups
            # then the current location must be operational
            return calc_config(condition[1:], groups[1:], 0)
        else:
            # if current group length doesn't match the first group in groups
            # and the group has started, then the current location must be broken
            if current_group:
                return calc_config(condition[1:], groups, current_group + 1)
            else:
                # if the group haven't started, then it doesn't have to start now
                return calc_config(
                    condition[1:], groups, current_group + 1
                ) + calc_config(condition[1:], groups, current_group)


def part2_modify(condition):
    modified_condition = list(condition)

    for i in range(4):
        modified_condition.extend(["?"] + list(condition))

    return tuple(modified_condition)


def main():
    with open("input12.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    lines = list(map(process_line, lines))

    total_config = 0
    # part 1
    for condition, groups in lines:
        total_config += calc_config(condition, groups)

    print(total_config)

    # part 2
    total_config = 0
    for condition, groups in lines:
        total_config += calc_config(part2_modify(condition), 5 * groups)

    print(total_config)


main()

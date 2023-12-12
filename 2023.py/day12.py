import itertools
import more_itertools as more
import utils

def process_line(line):
    line = line.split()

    return [i for i in line[0]], utils.ints(line[1])


def validate_config(condition, counts):
    groups = []
    current_group = 0

    for i in condition:
        if i == '#':
            current_group += 1
        else:
            if current_group:
                groups.append(current_group)
                current_group = 0

    if current_group:
        groups.append(current_group)

    return groups == counts


def calc_config(condition, counts):
    unknown_indices = [i for i in range(len(condition)) if condition[i] == '?']

    valid_config = 0

    for i in itertools.combinations_with_replacement([True, False], len(unknown_indices)):
        for config in more.distinct_permutations(i):
            new_condition = condition.copy()
            for is_spring, index in zip(config, unknown_indices):
                if is_spring:
                    new_condition[index] = '#'
            if validate_config(new_condition, counts):
                valid_config += 1
    
    return valid_config


def main():
    with open("input12.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    lines = list(map(process_line, lines))
    
    total_config = 0

    for condition, counts in lines:
        total_config += calc_config(condition, counts)

    print(total_config)

main()

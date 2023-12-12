import regex as re
import collections
import utils
from math import prod

DIGITS = [str(i) for i in range(0, 10)]
NON_SYMBOLS = DIGITS + ['.']

def validate_number(grid: utils.Grid, row_idx: int, match: re.match) -> bool:
    neighbors = set()
    for col_idx in range(*match.span()):
        neighbors.update(grid.get_adj_neighbors((row_idx, col_idx)))
    neighbor_items = [grid[coord] for coord in neighbors]
    return any([item not in NON_SYMBOLS for item in neighbor_items])


def search_gears(grid: utils.Grid, row_idx: int, match: re.match, gears: collections.defaultdict):
    neighbors = set()
    for col_idx in range(*match.span()):
        neighbors.update(grid.get_adj_neighbors((row_idx, col_idx)))
    adj_gears = [coord for coord in neighbors if grid[coord] == '*']
    
    for gear in adj_gears:
        gears[gear].append(int(match.group()))

    return None


def process_line(line) -> list[re.Match]:
    return list(re.finditer(r'\d+', line))


def main():
    with open("input03.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    
    # part 1
    grid = utils.Grid(lines)
    numbers = list(map(process_line, lines))
    part_number_sum = 0

    for row_idx, matches in enumerate(numbers):
        for match in matches:
            if validate_number(grid, row_idx, match):
                part_number_sum += int(match.group())

    print(part_number_sum)

    # part 2
    gear_to_numbers = collections.defaultdict(list)
    for row_idx, matches in enumerate(numbers):
        for match in matches:
            search_gears(grid, row_idx, match, gear_to_numbers)

    gear_ratio_sum = 0

    for numbers in gear_to_numbers.values():
        if len(numbers) == 2:
            gear_ratio_sum += prod(numbers)

    print(gear_ratio_sum)

    return None

main()

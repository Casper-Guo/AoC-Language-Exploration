import itertools
import utils
from typing import TypeAlias

Coord: TypeAlias = tuple[int, int]


def get_distance(galaxy1: Coord, galaxy2: Coord, expand_rows: set[int], expand_cols: set[int], expand_ratio) -> int:
    x1, y1 = galaxy1
    x2, y2 = galaxy2

    distance = abs(x1 - x2) + abs(y1 - y2)
    sorted_x = min(x1, x2), max(x1, x2)
    sorted_y = min(y1, y2), max(y1, y2)
    expand_amt = len([i for i in range(*sorted_x) if i in expand_rows]) + len([i for i in range(*sorted_y) if i in expand_cols])

    return distance + (expand_ratio - 1) * expand_amt


def main():
    with open("input11.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [[i for i in line] for line in lines]

    grid = utils.Grid(lines)
    no_galaxy_rows = set([i for i in range(grid.rows) if '#' not in grid.get_row(i)])
    no_galaxy_cols = set([i for i in range(grid.cols) if '#' not in grid.get_col(i)])
    galaxies = grid.find('#')

    part1_distance = 0

    # part 1
    for galaxy1, galaxy2 in itertools.combinations(galaxies, 2):
        part1_distance += get_distance(galaxy1, galaxy2, no_galaxy_rows, no_galaxy_cols, 2)

    print(part1_distance)

    # part 2
    part2_distance = 0
    for galaxy1, galaxy2 in itertools.combinations(galaxies, 2):
        part2_distance += get_distance(galaxy1, galaxy2, no_galaxy_rows, no_galaxy_cols, 1000000)

    print(part2_distance)
    return

main()

from itertools import product
from copy import deepcopy


def parse_line(line: str) -> list[int]:
    line = line.rstrip()
    return [0 if i == "." else 1 for i in line]


def validate_index(row: int, col: int, grid_size: int) -> bool:
    return 0 <= row < grid_size and 0 <= col < grid_size


def sum_neighbors(row: int, col: int, grid: list[list[int]]) -> int:
    deltas = [-1, 0, 1]
    total = 0
    size = len(grid)

    # part 2 only
    # keep the corner lights on
    if row == 0 or row == size - 1:
        if col == 0 or col == size - 1:
            return 2

    for delta_row, delta_col in product(deltas, repeat=2):
        if delta_row == 0 and delta_col == 0:
            continue
        if validate_index(row + delta_row, col + delta_col, size):
            total += grid[row + delta_row][col + delta_col]

    return total


def one_iter(grid: list[list[int]]) -> list[list[int]]:
    new_grid = deepcopy(grid)

    for row_idx, row in enumerate(grid):
        for col_idx, light in enumerate(row):
            neighbor_sum = sum_neighbors(row_idx, col_idx, grid)
            # print(row_idx, col_idx, neighbor_sum)

            if light == 0:
                if neighbor_sum == 3:
                    new_grid[row_idx][col_idx] = 1
            else:
                if neighbor_sum != 3 and neighbor_sum != 2:
                    new_grid[row_idx][col_idx] = 0

    return new_grid


def translate_grid(light: int) -> str:
    return "#" if light == 1 else "."


def print_grid(grid: list[list[int]]):
    print("\n".join(["".join([translate_grid(i) for i in row]) for row in grid]), "\n")


with open("input18.txt", "r") as f:
    input = f.readlines()

    # part 1 and part 2 differs in sum_neighbor implementation
    grid = [parse_line(line) for line in input]

    for i in range(100):
        grid = one_iter(grid)

    print(sum([sum(row) for row in grid]))

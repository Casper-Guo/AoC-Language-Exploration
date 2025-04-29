from collections import deque
from itertools import pairwise
from typing import Iterable, TypeAlias

import utils

Delta: TypeAlias = tuple[int, int]
Coord: TypeAlias = tuple[int, int]


PIPE_CONNECTIONS = {
    "|": ["N", "S"],
    "-": ["W", "E"],
    "L": ["N", "E"],
    "J": ["N", "W"],
    "7": ["S", "W"],
    "F": ["S", "E"],
    "S": ["N", "S", "E", "W"],
}

PIPE_CONNECTIONS = {
    pipe: [utils.CHAR_TO_DELTA[direction] for direction in directions]
    for pipe, directions in PIPE_CONNECTIONS.items()
}


def check_connected(current: str, next: str, direction: Delta) -> bool:
    """Direction is the delta from current to next. Check the two coordinates are connected."""
    if current not in PIPE_CONNECTIONS or next not in PIPE_CONNECTIONS:
        return False
    return (
        direction in PIPE_CONNECTIONS[current]
        and utils.turn_180(direction) in PIPE_CONNECTIONS[next]
    )


def expand_cycle(grid: utils.Grid, current: Coord) -> list[Coord]:
    next_coords = []
    for next in grid.get_dir_neighbors(current):
        if check_connected(grid[current], grid[next], utils.get_direction(next, current)):
            next_coords.append(next)
    return next_coords


def shoelace_formula(vertices: Iterable[Coord]) -> float:
    shoelace = 0
    for (x1, y1), (x2, y2) in pairwise(vertices + vertices[:1]):
        shoelace += (x1 * y2) - (y1 * x2)
    return abs(shoelace) / 2


def main():
    with open("input10.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [list(line) for line in lines]

    # part 1
    grid = utils.Grid(lines)
    start = grid.find("S")[0]
    cycle = {start: 0}
    step = 0
    current_coords = deque([start])

    while current_coords:
        step += 1
        current_coord = current_coords.pop()
        next_coords = list(filter(lambda x: x not in cycle, expand_cycle(grid, current_coord)))[
            :1
        ]
        for next_coord in next_coords:
            cycle[next_coord] = step
        current_coords.extend(next_coords)

    print(step / 2)

    # part 2 geometry solution
    # sort vertices by their order of appearance in the cycle
    vertices = sorted(cycle.items(), key=lambda x: x[1])
    vertices = [vertex[0] for vertex in vertices]

    # Shoelace Formula
    internal_area = shoelace_formula(vertices)

    # Pick's Theorem
    print(internal_area + 1 - (len(vertices) / 2))

    # part 2 even-odd rule solution
    # hardcode to replace S with the actual pipe configuration
    grid[start] = "J"

    inside = False
    inside_count = 0

    for coord in grid.coords():
        if coord in cycle:
            if utils.CHAR_TO_DELTA["N"] in PIPE_CONNECTIONS[grid[coord]]:
                inside = not inside
        else:
            if inside:
                inside_count += 1

    print(inside_count)
    return


main()

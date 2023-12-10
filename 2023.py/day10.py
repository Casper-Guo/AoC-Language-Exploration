from collections import deque
import utils
from typing import TypeAlias

Delta: TypeAlias = tuple[int, int]
Coord: TypeAlias = tuple[int, int]


PIPE_CONNECTIONS = {
    '|': ['N', 'S'],
    '-': ['W', 'E'],
    'L': ['N', 'E'],
    'J': ['N', 'W'],
    '7': ['S', 'W'],
    'F': ['S', 'E'],
    'S': ['N', 'S', 'E', 'W']
}

PIPE_CONNECTIONS = {pipe:[utils.CHAR_TO_DELTA[direction] for direction in directions] for pipe, directions in PIPE_CONNECTIONS.items()}


def reverse_direction(direction: Delta) -> Delta:
    return -direction[0], -direction[1]


def find_direction(current:Coord, next:Coord) -> Delta:
    """Find the direction vector from current to next."""
    return next[0] - current[0], next[1] - current[1]


def check_connected(current: str, next: str, direction: Delta) -> bool:
    """Direction is the delta from current to next. Check the two coordinates are connected."""
    if current not in PIPE_CONNECTIONS or next not in PIPE_CONNECTIONS:
        return False
    return direction in PIPE_CONNECTIONS[current] and reverse_direction(direction) in PIPE_CONNECTIONS[next]


def expand_cycle(grid: utils.Grid, current: Coord) -> list[Coord]:
    next_coords = []
    for next in grid.get_dir_neighbors(current):
        if check_connected(grid[current], grid[next], find_direction(current, next)):
            next_coords.append(next)
    return next_coords


def main():
    with open("input10.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    
    grid = utils.Grid(lines)
    start = grid.find('S')[0]
    cycle = {start: 0}
    step = 0
    current_coords = set([start])

    while current_coords:
        step += 1
        new_current = set()
        for current_coord in current_coords:
            next_coords = list(filter(lambda x: x not in cycle, expand_cycle(grid, current_coord)))

            for next_coord in next_coords:
                cycle[next_coord] = step

            new_current.update(next_coords)
        
        current_coords = new_current

    print(step - 1)
    return

main()

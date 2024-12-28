from collections import defaultdict
from typing import TypeAlias

import utils
from heapdict import heapdict

Coord: TypeAlias = tuple[int, int]
Direction: TypeAlias = tuple[int, int]


def process_line(line):
    return [int(i) for i in line]


def get_neighbors(
    grid: utils.Grid, current: Coord, travel_direction: Direction, travel_amt: int, part1: bool
):
    neighbors = []

    if travel_direction == (0, 0):
        for direction in utils.DELTA_TO_UDLR:
            neighbors.append((*utils.change_direction(current, direction), 1))
    else:
        if part1:
            neighbors.append(
                (*utils.change_direction(current, utils.turn_left(travel_direction)), 1)
            )
            neighbors.append(
                (*utils.change_direction(current, utils.turn_right(travel_direction)), 1)
            )

            if travel_amt < 3:
                neighbors.append(
                    (*utils.change_direction(current, travel_direction), travel_amt + 1)
                )
        else:
            if travel_amt < 4:
                neighbors.append(
                    (*utils.change_direction(current, travel_direction), travel_amt + 1)
                )
            else:
                neighbors.append(
                    (*utils.change_direction(current, utils.turn_left(travel_direction)), 1)
                )
                neighbors.append(
                    (*utils.change_direction(current, utils.turn_right(travel_direction)), 1)
                )

                if travel_amt < 10:
                    neighbors.append(
                        (*utils.change_direction(current, travel_direction), travel_amt + 1)
                    )

    return list(filter(lambda x: x[0] in grid, neighbors))


def extract_coord(dist, coord, part1):
    if part1:
        return list(filter(lambda x: x[0][0] == coord, dist.items()))
    return list(filter(lambda x: x[0][0] == coord and x[0][2] >= 4, dist.items()))


def dijkstra(grid: utils.Grid, start: Coord, part1: bool):
    dist = defaultdict(lambda: 10**8)
    dist[(start, (0, 0), 0)] = 0

    queue = heapdict()
    queue[(start, (0, 0), 0)] = 0

    while queue:
        min_node, current_dist = queue.popitem()
        current_coord, travel_direction, travel_amt = min_node

        for next in get_neighbors(grid, current_coord, travel_direction, travel_amt, part1):
            next_coord, direction, amt = next
            loss = current_dist + grid[next_coord]

            if loss < dist[next]:
                dist[next] = loss
                queue[next] = loss
            elif loss == dist[next]:
                queue[next] = loss

    return dist


def main():
    with open("input17.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    lines = list(map(process_line, lines))
    grid = utils.Grid(lines)

    dist = dijkstra(grid, (0, 0), True)
    states = extract_coord(dist, (grid.rows - 1, grid.cols - 1), True)
    print(min([i[-1] for i in states]))

    dist = dijkstra(grid, (0, 0), False)
    states = extract_coord(dist, (grid.rows - 1, grid.cols - 1), False)
    print(min([i[-1] for i in states]))
    return


main()

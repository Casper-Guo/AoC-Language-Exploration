from collections import deque
from copy import deepcopy
from functools import lru_cache
from typing import TypeAlias

import matplotlib.pyplot as plt
import networkx as nx
import utils

WGraph: TypeAlias = dict[utils.Coord, dict[utils.Coord, int]]


SLOPE_DIRS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}


def get_next_coords(grid: utils.Grid[str], current: utils.Coord) -> list[utils.Coord]:
    if grid[current] == "#":
        return []

    if grid[current] == ".":
        return [
            neighbor
            for neighbor in grid.get_dir_neighbors(current)
            if grid[neighbor] == "."
            or (
                grid[neighbor] in SLOPE_DIRS
                and utils.get_direction(neighbor, current) == SLOPE_DIRS[grid[neighbor]]
            )
        ]

    return [utils.change_direction(current, SLOPE_DIRS[grid[current]])[0]]


def is_intersection(grid: utils.Grid[str], coord: utils.Coord) -> bool:
    if grid[coord] == "#":
        return False
    return (
        len(
            [
                next
                for next in grid.get_dir_neighbors(coord)
                if (grid[next] == "." or grid[next] in SLOPE_DIRS)
            ]
        )
        >= 3
    )


def one_hop_explore(
    grid: utils.Grid[str],
    start_coord: utils.Coord,
    special_coords: set[utils.Coord],
) -> dict[utils.Coord, int]:
    """Get the distance to the nearest intersections or special coords."""
    dists: dict[utils.Coord, int] = {}
    visited: set[utils.Coord] = {start_coord}
    to_visit = deque([(next_coord, 1) for next_coord in get_next_coords(grid, start_coord)])

    while len(to_visit):
        current, num_steps = to_visit.popleft()
        visited.add(current)
        if is_intersection(grid, current) or current in special_coords:
            dists[current] = num_steps
        else:
            for next_coord in get_next_coords(grid, current):
                if next_coord not in visited:
                    to_visit.append((next_coord, num_steps + 1))

    return dists


def make_dag(grid: utils.Grid[str]) -> WGraph:
    path_coords = grid.find(".")
    start, end = path_coords[0], path_coords[-1]
    graph = {
        start: one_hop_explore(grid, start, {start, end}),
    }

    for intersection in [coord for coord in grid.coords() if is_intersection(grid, coord)]:
        graph[intersection] = one_hop_explore(grid, intersection, {start, end})

    return graph


def to_networkx(graph: WGraph) -> nx.DiGraph:
    digraph = nx.DiGraph()
    for src, neighbors in graph.items():
        for dst, weight in neighbors.items():
            digraph.add_edge(src, dst, weight=weight)
    return digraph


def visualize_graph(graph: nx.DiGraph) -> None:
    pos = {node: (node[1], -node[0]) for node in graph.nodes()}
    edge_labels = nx.get_edge_attributes(graph, "weight")

    plt.figure(figsize=(10, 8))
    nx.draw(graph, pos, with_labels=True, arrows=True)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.savefig("graph.png")


def part1(graph: WGraph, start: utils.Coord, end: utils.Coord) -> int:
    @lru_cache
    def dag_longest_path_length(current: utils.Coord) -> int:
        if current == end:
            return 0
        return max(
            dag_longest_path_length(neighbor) + weight
            for neighbor, weight in graph[current].items()
        )

    return dag_longest_path_length(start)


def dag_to_simple(graph: WGraph) -> WGraph:
    simple_graph: WGraph = deepcopy(graph)

    for src, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            if neighbor not in simple_graph:
                simple_graph[neighbor] = {src: weight}
            simple_graph[neighbor][src] = weight

    return simple_graph


def part2(graph: WGraph, start: utils.Coord, end: utils.Coord) -> int:
    def part2_helper(path: set[utils.Coord], current: utils.Coord) -> int:
        if current == end:
            return 0

        max_length = -10000
        for neighbor, weight in graph[current].items():
            if neighbor not in path:
                path.add(neighbor)
                max_length = max(
                    max_length,
                    part2_helper(path, neighbor) + weight,
                )
                path.remove(neighbor)
        return max_length

    return part2_helper({start}, start)


def main() -> None:
    with open("input23.txt", "r") as f:
        lines = [list(line.strip()) for line in f.readlines()]

    grid = utils.Grid(lines)
    path_coords = grid.find(".")
    start, end = path_coords[0], path_coords[-1]
    graph = make_dag(grid)

    print(part1(graph, start, end))
    print(part2(dag_to_simple(graph), start, end))


if __name__ == "__main__":
    main()

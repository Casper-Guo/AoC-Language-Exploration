from collections import defaultdict, deque
import utils

SLOPES = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}


def get_next_coords(grid, current):
    if grid[current] == ".":
        next_coords = []
        neighbors = grid.get_dir_neighbors(current)
        for neighbor in neighbors:
            if grid[neighbor] == ".":
                next_coords.append(neighbor)
            elif grid[neighbor] in SLOPES:
                if utils.get_direction(neighbor, current) == SLOPES[grid[neighbor]]:
                    next_coords.append(neighbor)
        return next_coords

    return [utils.change_direction(current, SLOPES[grid[current]])[0]]


def bfs(grid, start):
    visited = defaultdict(set)
    visited[start].add(0)
    num_steps = 0

    next_coords = deque(get_next_coords(grid, start))

    while next_coords:
        num_steps += 1

        nexts = set()
        while next_coords:
            current = next_coords.pop()
            visited[current].add(num_steps)
            next = get_next_coords(grid, current)
            unvisited = list(filter(lambda x: num_steps - 1 not in visited[x], next))
            nexts.update(unvisited)

        next_coords = deque(nexts)

    return visited


def main():
    with open("input23.txt", "r") as f:
        lines = f.readlines()
        lines = [[i for i in line.strip()] for line in lines]
    grid = utils.Grid(lines)
    start = grid.find(".")[0]
    end = grid.find(".")[-1]

    # part 1
    step_counts = bfs(grid, start)
    print(max(step_counts[end]))

    # part 2

    return


main()

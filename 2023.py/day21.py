import utils


def reachable_garden_plots(grid, current):
    return [i for i in grid.get_dir_neighbors(current) if grid[i] == "."]


def main():
    with open("input21.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [list(line) for line in lines]

    grid = utils.Grid(lines)
    start = grid.find("S")[0]
    grid[start] = "."

    # part 1
    reached = {start}
    steps = 0
    step_limit = 64

    while steps < step_limit:
        next_step = set()
        for plot in reached:
            next_step.update(reachable_garden_plots(grid, plot))

        reached = next_step
        steps += 1

    print(len(reached))
    return


main()

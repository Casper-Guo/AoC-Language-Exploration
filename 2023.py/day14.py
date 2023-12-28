import utils


def let_roll(line: list[str]) -> list[str]:
    """Let rocks roll all the way to the left."""
    for initial, i in enumerate(line):
        if i == "O":
            for final in range(initial - 1, -1, -1):
                if line[final] != '.':
                    line[initial] = "."
                    line[final + 1] = "O"
                    break
            else:
                line[initial] = "."
                line[0] = "O"

    return line


def calc_load(line: list[str]) -> int:
    return sum(
        map(lambda x: len(line) - x, [i for i in range(len(line)) if line[i] == "O"])
    )


def cycle(grid):
    # roll north
    new_lines = [let_roll(grid.get_col(i)) for i in range(grid.cols)]
    grid.grid = new_lines
    grid.transpose()

    # roll west
    new_lines = [let_roll(grid.get_row(i)) for i in range(grid.rows)]
    grid.grid = new_lines

    # roll south
    new_lines = [let_roll(list(reversed(grid.get_col(i)))) for i in range(grid.cols)]
    grid.grid = new_lines
    grid.rotate_left_90()

    # roll east
    new_lines = [let_roll(list(reversed(grid.get_row(i)))) for i in range(grid.rows)]
    new_lines = [list(reversed(line)) for line in new_lines]
    grid.grid = new_lines

    return grid


def main():
    with open("input14.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [[i for i in line] for line in lines]

    grid = utils.Grid(lines)
    print(sum(map(calc_load, [let_roll(grid.get_col(i)) for i in range(grid.cols)])))

    for i in range(200):
        grid = cycle(grid)

    print(sum(map(calc_load, [grid.get_col(i) for i in range(grid.cols)])))

    return


main()

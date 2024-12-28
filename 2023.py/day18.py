import regex as re
import utils


def shoelace(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    return (x1 * y2 - y1 * x2) / 2


def move_coord(start, move, amt):
    return start[0] + amt * move[0], start[1] + amt * move[1]


def process_line(line):
    search = re.search(r"(\w{1}) (\d+) \(\#(.+)\)", line)
    return search.group(1), int(search.group(2)), search.group(3)


def find_area(instructions):
    start = (0, 0)
    num_edge_points = 0
    internal_area = 0

    for direction, amt in instructions:
        num_edge_points += amt
        end = move_coord(start, utils.CHAR_TO_DELTA[direction], amt)
        internal_area += shoelace(start, end)
        start = end

    internal_points = abs(internal_area) + 1 - (num_edge_points / 2)
    return num_edge_points + internal_points


def main():
    with open("input18.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    lines = list(map(process_line, lines))

    # part 1
    print(find_area(zip([line[0] for line in lines], [line[1] for line in lines])))

    # part 2
    num_to_direction = {"0": "R", "1": "D", "2": "L", "3": "U"}
    part2_directions = [num_to_direction[line[2][-1]] for line in lines]
    part2_amts = [int(line[2][:-1], 16) for line in lines]

    print(find_area(zip(part2_directions, part2_amts)))
    return


main()

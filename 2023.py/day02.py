import math


def count_marble(marble_set: list[str]) -> tuple[int]:
    """Take ['3 green', '2 blue', '1 red'] to (1, 3, 2)."""
    # order: rgb
    counts = [0, 0, 0]

    for color in marble_set:
        color = color.split()
        count = int(color[0])
        color = color[1]

        if color == "red":
            counts[0] = count
        elif color == "green":
            counts[1] = count
        elif color == "blue":
            counts[2] = count

    return tuple(counts)


def process_line(line: str) -> list[tuple[int]]:
    """First line of sample input is converted to [(4, 0, 3), (1, 2, 6), (0, 2, 0)]."""
    line = line[line.find(":") + 2:]

    # split into sets
    sets = line.split(";")

    # split into number and color combos
    sets = map(lambda x: x.split(", "), sets)

    return list(map(count_marble, sets))


def validate_game(max_marble: tuple[int], game: list[tuple[int]]) -> bool:
    possible = True

    for one_set in game:
        for max, count in zip(max_marble, one_set):
            if count > max:
                possible = False

    return possible


def min_marble_power(game: list[tuple[int]]) -> int:
    min_marbles = [max(max(color), 1) for color in zip(*game)]

    return math.prod(min_marbles)


def main():
    with open("input02.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    lines = list(map(process_line, lines))

    # order: rgb
    max_possible = (12, 13, 14)

    id_sum = 0
    min_power_sum = 0

    for idx, line in enumerate(lines):
        if validate_game(max_possible, line):
            id_sum += idx + 1
        min_power_sum += min_marble_power(line)

    print(id_sum)
    print(min_power_sum)

    return


main()

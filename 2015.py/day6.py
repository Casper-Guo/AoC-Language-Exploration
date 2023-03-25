def process_line(line: str) -> tuple[str, tuple[int, int], tuple[int, int]]:
    # replace the two commas with spaces
    line = line.replace(',', ' ', 2)

    # split the line by spaces
    # last twi is always second coordinate
    # then through
    # then next two is the first coordinate
    # then the instruction
    words = line.split()

    return ' '.join(words[:-5]), (int(words[-5]), int(words[-4])), (int(words[-2]), int(words[-1]))


def switch_on_off(instruction: str,
                  coordinate_1: tuple[int, int],
                  coordinate_2: tuple[int, int],
                  status: dict[tuple[int, int], bool]
                  ) -> None:
    x1, y1 = coordinate_1
    x2, y2 = coordinate_2

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if instruction == "turn on":
                status[(x, y)] = True
            elif instruction == "turn off":
                status[(x, y)] = False
            elif instruction == "toggle":
                status[(x, y)] = not status.get((x, y), False)


def change_brightness(instruction: str,
                      coordinate_1: tuple[int, int],
                      coordinate_2: tuple[int, int],
                      brightness: dict[tuple[int, int], int]
                      ) -> None:
    x1, y1 = coordinate_1
    x2, y2 = coordinate_2

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if instruction == "turn on":
                brightness[(x, y)] = brightness.get((x, y), 0) + 1
            elif instruction == "turn off":
                brightness[(x, y)] = max(0, brightness.get((x, y), 0) - 1)
            elif instruction == "toggle":
                brightness[(x, y)] = brightness.get((x, y), 0) + 2


with open("input6.txt", 'r') as f:
    # part 1
    status = {}
    instructions = f.readlines()

    for instruction in instructions:
        switch_on_off(*process_line(instruction), status)

    on_count = 0

    for light in status.values():
        if light:
            on_count += 1

    print(on_count)

    # part 2
    brightness = {}

    for instruction in instructions:
        change_brightness(*process_line(instruction), brightness)

    total_brightness = sum(brightness.values())
    print(total_brightness)

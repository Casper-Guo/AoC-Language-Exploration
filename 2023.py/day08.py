import regex as re
from math import lcm


def process_line(line):
    capture = re.findall(r"[1-9A-Z]{3}", line)
    return capture


def move_one(current, steps, instruction, network):
    if instruction[steps % len(instruction)] == "L":
        return network[current][0]
    else:
        return network[current][1]


def main():
    with open("input08.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    instruction = lines[0]
    lines = list(map(process_line, lines[2:]))
    network = {line[0]: (line[1], line[2]) for line in lines}

    current = "AAA"
    steps = 0

    # part 1
    while current != "ZZZ":
        current = move_one(current, steps, instruction, network)
        steps += 1

    print(steps)

    # part 2
    ghost_start = [line[0] for line in lines if line[0].endswith("A")]
    num_steps = []

    for start in ghost_start:
        steps = 0
        while not start.endswith("Z"):
            start = move_one(start, steps, instruction, network)
            steps += 1
        num_steps.append(steps)

    print(lcm(*num_steps))
    return


main()

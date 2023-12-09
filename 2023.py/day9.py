import itertools
import utils

def process_line(line):
    return utils.ints(line)


def condense(line):
    return list((b - a for a, b in itertools.pairwise(line)))


def extrapolate(line, condensed_line):
    return line + [line[-1] + condensed_line[-1]]


def extrapolate_left(line, condensed_line):
    return [line[0] - condensed_line[0]] + line


def main():
    with open("input9.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    lines = list(map(process_line, lines))

    # part 1
    sum_extrapolated = 0
    for line in lines:
        condensing = [line]
        while not all(i == 0 for i in line):
            line = condense(line)
            condensing.append(line)
        for condensed, prior in itertools.pairwise(reversed(condensing)):
            line = extrapolate(prior, condensed)
        sum_extrapolated += line[-1]

    print(sum_extrapolated)

    # part 2
    lines = [line[:-1] for line in lines]
    sum_extrapolated = 0

    for line in lines:
        condensing = [line]
        while not all(i == 0 for i in line):
            line = condense(line)
            condensing.append(line)

        new_line = condensing[-1]
            
        for _, line in itertools.pairwise(reversed(condensing)):
            new_line = extrapolate_left(line, new_line)
        sum_extrapolated += new_line[0]

    print(sum_extrapolated)
        
    return

main()

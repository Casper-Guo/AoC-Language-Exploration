import regex as re
import utils


def process_line(line):
    return [int(i) for i in line if i.isdigit()]


def find_digits(line):
    digits = list(utils.DIGITS.keys()) + [str(i) for i in range(1, 10)]
    matches = re.findall("|".join(digits), line, overlapped=True)

    first, last = matches[0], matches[-1]

    first = utils.DIGITS[first] if first in utils.DIGITS else int(first)
    last = utils.DIGITS[last] if last in utils.DIGITS else int(last)

    return first, last


def main():
    with open("input01.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    # part 1
    ints = list(map(process_line, lines))
    print(sum(map(lambda x: x[0] * 10 + x[-1], ints)))

    # part 2
    digits = list(map(find_digits, lines))
    print(sum(map(lambda x: x[0] * 10 + x[-1], digits)))

    return


main()

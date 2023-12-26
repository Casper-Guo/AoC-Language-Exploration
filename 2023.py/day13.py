from collections import defaultdict
import utils


def diff_count(left, right) -> bool:
    return len([i for i in range(len(left)) if left[i] != right[i]])


def find_reflections(
    equivs: defaultdict[int, set[int]],
    offs: defaultdict[int, set[int]],
    length: int,
    part1: bool,
):
    reflections = []

    for reflect_line in range(1, length):
        # reflect line 1 is between row/col 0 and 1
        # so on and so forth until length - 1
        valid = True
        fixed_smudge = False
        for offset in range(min(reflect_line, length - reflect_line)):
            line1 = reflect_line + offset
            line2 = reflect_line - offset - 1

            if line1 not in equivs[line2]:
                valid = False

                if not part1:
                    # extra logic for part2
                    if not fixed_smudge:
                        if line1 in offs[line2]:
                            valid = True
                            fixed_smudge = True
                        else:
                            # more than one differences between the two lines
                            break
                    else:
                        # a smudge elsewhere is already fixed
                        break
        if (part1 and valid) or (not part1 and valid and fixed_smudge):
            reflections.append(reflect_line)

    return reflections


def summarize_pattern(pattern: utils.Grid, part1: bool) -> float:
    row_equiv = defaultdict(set)
    row_off = defaultdict(set)
    col_equiv = defaultdict(set)
    col_off = defaultdict(set)

    for i in range(pattern.rows):
        for j in range(i + 1, pattern.rows):
            num_diff = diff_count(pattern.get_row(i), pattern.get_row(j))
            if num_diff == 0:
                row_equiv[i].add(j)
                row_equiv[j].add(i)
            elif num_diff == 1:
                row_off[i].add(j)
                row_off[j].add(i)

    for i in range(pattern.cols):
        for j in range(i + 1, pattern.cols):
            num_diff = diff_count(pattern.get_col(i), pattern.get_col(j))
            if num_diff == 0:
                col_equiv[i].add(j)
                col_equiv[j].add(i)
            elif num_diff == 1:
                col_off[i].add(j)
                col_off[j].add(i)

    vertical_sum = sum(find_reflections(col_equiv, col_off, pattern.cols, part1))
    horizontal_sum = (
        sum(find_reflections(row_equiv, row_off, pattern.rows, part1)) * 100
    )

    return vertical_sum + horizontal_sum


def main():
    with open("input13.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    patterns = list(map(lambda x: utils.Grid(x), utils.list_split(lines, "")))

    part1_total = sum([summarize_pattern(pattern, True) for pattern in patterns])
    part2_total = sum([summarize_pattern(pattern, False) for pattern in patterns])

    print(part1_total)
    print(part2_total)
    return


main()

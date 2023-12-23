import utils
from copy import deepcopy


def check_overlap(range1, range2):
    # the ranges are inclusive
    start1, end1 = range1
    start2, end2 = range2

    if start1 < start2:
        return end1 >= start2
    else:
        return start1 <= end2


def is_support(brick1, brick2):
    if brick1[5] != brick2[2] - 1:
        # if the top of brick1 is not one below the bottom of brick2
        # then brick1 definitely doesn't support brick2
        return False 
    
    return check_overlap((brick1[0], brick1[3]), (brick2[0], brick2[3])) and check_overlap((brick1[1], brick1[4]), (brick2[1], brick2[4]))


def process_line(line):
    return tuple(utils.ints(line))


def simulate(bricks):
    supports = {brick:set() for brick in bricks if brick[2] == 1}
    falling = set(filter(lambda x: x[2] != 1, bricks))

    while falling:
        iter = deepcopy(falling)
        for brick in sorted(falling, key=lambda x: x[2]):
            iter.remove(brick)

            if brick[2] == 1:
                # landed
                supports[brick] = set()
            else:
                supported = False
                for support in supports:
                    if is_support(support, brick):
                        supports[support].add(brick)
                        supported = True
                if supported:
                    supports[brick] = set()
                else:
                    brick = list(brick)
                    brick[2] -= 1
                    brick[5] -= 1
                    iter.add(tuple(brick))
        falling = iter

    return supports


def find_num_fall(brick, supports, supported):
    if len(supports[brick]) == 0:
        return 0

    num_fall = 0
    for i in supported:
        supported[i] -= set([brick])

    for i in supports[brick]:
        if len(supported[i]) == 0:
            num_fall += 1 + find_num_fall(i, supports, supported)
    return num_fall


def main():
    with open("input22.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    bricks = list(map(process_line, lines))
    supports = simulate(bricks)
    supported = utils.dict_transpose(supports)

    num_disintegratable = 0
    for supporting in supports.values():
        num_supports = [len(supported[i]) for i in supporting]
        num_disintegratable += all(num > 1 for num in num_supports)

    print(num_disintegratable)

    num_fall = 0
    for brick in supports:
        num_fall += find_num_fall(brick, deepcopy(supports), deepcopy(supported))

    print(num_fall)
    return

main()

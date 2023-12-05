import regex as re
import itertools
import more_itertools as more
from collections import defaultdict, Counter
import utils
from math import prod

def process_maps(maps):
    for idx, mapping in enumerate(maps):
        numbers = mapping.split('\n')[1:]
        maps[idx] = [tuple(utils.ints(number)) for number in numbers]
    
    return maps


def seed_to_location(seed, mappings):
    for mapping in mappings:
        for dest_start, source_start, length in mapping:
            if 0 <= (seed - source_start) <= length:
                seed = seed - source_start + dest_start
                break
    return seed


def process_seeds(seeds):
    return list(more.windowed(utils.ints(seeds), 2, step=2))


def main():
    with open("input5.txt", "r") as f:
        lines = f.read().split('\n\n')

    # part 1
    part1_seeds = utils.ints(lines[0])
    maps = process_maps(lines[1:])

    part1_seeds = list(map(lambda seed: seed_to_location(seed, maps), part1_seeds))
    print(min(part1_seeds))

    # part 2
    part2_seeds = process_seeds(lines[0])
    return

main()

import more_itertools as more
import utils


def process_mappings(mappings: list[str]) -> list[list[tuple[int]]]:
    for idx, mapping in enumerate(mappings):
        numbers = mapping.split("\n")[1:]
        mappings[idx] = [tuple(utils.ints(number)) for number in numbers]

    return mappings


def seed_to_location(seed: list[int], mappings: list[list[tuple[int]]]) -> list[int]:
    for mapping in mappings:
        for dest_start, source_start, length in mapping:
            if 0 <= (seed - source_start) <= length - 1:
                seed = seed - source_start + dest_start
                break
    return seed


def process_seeds(seeds: str) -> list[tuple[int]]:
    seed_intervals = []
    for interval in more.windowed(utils.ints(seeds), 2, step=2):
        start, length = interval
        seed_intervals.append((start, start + length - 1))

    return sorted(seed_intervals)


def check_overlap(left: tuple[int], right: tuple[int]) -> bool:
    left_start, left_end = left
    right_start, right_end = right

    if left_start <= right_start:
        return left_end >= right_start
    return left_start <= right_end


def collapse_once(intervals: list[tuple[int]]) -> list[tuple[int]]:
    if len(intervals) <= 1:
        return intervals
    if len(intervals) == 2:
        if check_overlap(*intervals):
            return [(intervals[0][0], max(intervals[0][1], intervals[1][1]))]
        return intervals

    mid = len(intervals) // 2
    return collapse_once(intervals[:mid]) + collapse_once(intervals[mid:])


def collapse_intervals(intervals: list[tuple[int]]) -> list[tuple[int]]:
    intervals = sorted(intervals)
    current_length = len(intervals)
    new_length = 0

    while current_length != new_length:
        current_length = new_length
        intervals = collapse_once(intervals)
        new_length = len(intervals)

    return intervals


def map_intervals(intervals: list[tuple[int]], mappings: list[tuple[int]]) -> list[tuple[int]]:
    new_intervals = set()

    for interval in intervals:
        interval_start, interval_end = interval
        interval_length = interval_end - interval_start + 1
        relevant_mappings = [
            i for i in mappings if check_overlap(interval, (i[1], i[1] + i[2] - 1))
        ]

        if not relevant_mappings:
            new_intervals.add(interval)
            continue

        not_mapped_start, not_mapped_end = interval_start, relevant_mappings[0][1] - 1
        for dest_start, source_start, length in relevant_mappings:
            source_end = source_start + length - 1
            not_mapped_end = source_start - 1
            if not_mapped_end > not_mapped_start and not_mapped_start <= interval_end:
                new_intervals.add((not_mapped_start, min(interval_end, not_mapped_end)))

            # three cases
            # 1, entire mapping interval is in the current interval
            # 2, the two intervals overlap partially (left overlap or right overlap)
            # 3, entire current interval is in the mapping interval
            mapped_interval_length = min(
                length,
                interval_end - source_start + 1,
                source_end - interval_start + 1,
                interval_length,
            )
            mapped_interval_start = (
                dest_start + max(interval_start, source_start) - source_start
            )
            new_intervals.add(
                (
                    mapped_interval_start,
                    mapped_interval_start + mapped_interval_length - 1,
                )
            )

            not_mapped_start = source_end + 1

        if not_mapped_start <= interval_end:
            new_intervals.add((not_mapped_start, interval_end))

    return list(new_intervals)


def main():
    with open("input05.txt", "r") as f:
        lines = f.read().split("\n\n")

    # part 1
    part1_seeds = utils.ints(lines[0])
    mappings = process_mappings(lines[1:])
    mappings = [sorted(mapping, key=lambda x: x[1]) for mapping in mappings]

    part1_seeds = [seed_to_location(seed, mappings) for seed in part1_seeds]
    print(min(part1_seeds))

    # part 2
    part2_seeds = process_seeds(lines[0])

    for mapping in mappings:
        part2_seeds = collapse_intervals(map_intervals(part2_seeds, mapping))

    print(sorted(part2_seeds)[0][0])

    return


main()

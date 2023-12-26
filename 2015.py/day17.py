def count_combos(target: int, used: list[int], unused: list[int]) -> int:
    global all_combos

    if sum(used) > target:
        return 0
    if sum(used) == target:
        all_combos.append(used)
        return 1

    total = 0

    for idx, bucket in enumerate(unused):
        new_used = used + [bucket]
        new_unused = unused[idx + 1 :]
        total += count_combos(target, new_used, new_unused)

    return total


with open("input17.txt", "r") as f:
    input = f.readlines()
    buckets = [int(line.strip()) for line in input]

    all_combos = []
    print(count_combos(150, [], buckets))

    min_bucket = 100
    min_count = 0

    for combo in all_combos:
        if len(combo) < min_bucket:
            min_bucket = len(combo)
            min_count = 1
        elif len(combo) == min_bucket:
            min_count += 1

    print(min_count)

from itertools import combinations


def parse_line(line: str) -> tuple[str, str, int]:
    splits = line.strip('\n.').split()

    if splits[2] == 'gain':
        return splits[0], splits[-1], int(splits[3])
    elif splits[2] == 'lose':
        return splits[0], splits[-1], -int(splits[3])


def find_gain(start: str, end: str, relationship: dict[str, dict[str, int]]) -> int:
    return relationship[start][end] + relationship[end][start]


def held_karp(relationship: dict) -> int:
    people = list(relationship.keys())

    n = len(people)

    g = {}

    for k in range(1, n):
        g[tuple([tuple([k]), k])] = find_gain(
            people[0], people[k], relationship)

    for s in range(2, n):
        for S in combinations(range(1, n), s):
            for k in S:
                options = []
                for m in S:
                    if m == k:
                        continue
                    m_k = find_gain(people[m], people[k], relationship)

                    S_not_k = tuple([i for i in S if i != k])
                    options.append(g[(S_not_k, m)] + m_k)

                g[(S, k)] = max(options)

    paths = []

    for k in range(1, n):
        k_1 = find_gain(people[0], people[k], relationship)
        paths.append(g[tuple([tuple(i for i in range(1, n)), k])] + k_1)

    return max(paths)


with open("input.txt", "r") as f:
    input = f.readlines()
    relationship = {}

    # part 1
    for line in input:
        start, end, delta = parse_line(line)

        if start not in relationship:
            relationship[start] = {end: delta}
        else:
            relationship[start][end] = delta

    print(held_karp(relationship))

    # part 2
    relationship['Casper'] = {}
    for people in relationship:
        relationship[people]['Casper'] = 0
        relationship['Casper'][people] = 0

    print(held_karp(relationship))

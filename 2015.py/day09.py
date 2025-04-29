# Note: given the input size, it is totally acceptable to brute force this

from itertools import combinations


def parse_line(line: str) -> tuple[str, str, int]:
    words = line.strip().split()

    return words[0], words[2], int(words[-1])


def lookup_dist(start: str, end: str, dist: dict) -> int:
    assert start in dist and end in dist
    if start == end:
        return 0
    try:
        return dist[start][end]
    except KeyError:
        # return a large dist for unconnected cities
        # so the path is not considered (hopefully)
        return 10000


def held_karp(graph: dict) -> int:
    # for part 1, just change the max to min
    cities = list(graph.keys())

    # swap dummy city to be the first point
    # designated starting point
    cities = ["dummy"] + cities[:-1]

    n = len(cities)

    g = {}

    for k in range(1, n):
        g[((k,), k)] = lookup_dist(cities[0], cities[k], graph)

    for s in range(2, n):
        for S in combinations(range(1, n), s):  # noqa: N806
            for k in S:
                options = []
                for m in S:
                    if m == k:
                        continue
                    m_k = lookup_dist(cities[m], cities[k], graph)

                    S_not_k = tuple([i for i in S if i != k])  # noqa: N806
                    options.append(g[(S_not_k, m)] + m_k)

                g[(S, k)] = max(options)

    paths = []

    for k in range(1, n):
        # distance to desginated start (dummy)
        # is always 0
        paths.append(g[(tuple(i for i in range(1, n)), k)])

    return max(paths)


with open("input09.txt", "r") as f:
    graph = {}
    input = f.readlines()

    for line in input:
        start, end, dist = parse_line(line)

        if start not in graph:
            graph[start] = {end: dist}
        else:
            graph[start][end] = dist

        if end not in graph:
            graph[end] = {start: dist}
        else:
            graph[end][start] = dist

    # add dummy city for Held-Karp
    graph["dummy"] = {}
    for city in graph:
        graph["dummy"][city] = 0
        graph[city]["dummy"] = 0

    print(held_karp(graph))

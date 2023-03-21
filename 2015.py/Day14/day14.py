def parse_line(line: str) -> list[int]:
    return [int(i) for i in line.split() if i.isdigit()]


def find_distance(time: int, speed: int, flight_duration: int, rest: int) -> int:
    period = flight_duration + rest
    full_periods = time // period
    remaining = time - full_periods * period

    return full_periods * speed * flight_duration + speed * min(flight_duration, remaining)


def new_score(time: int, reindeers: list[tuple[int, int, int]]) -> list[int]:
    scores = [0] * len(reindeers)

    for i in range(1, time):
        distances = [find_distance(i, *reindeer) for reindeer in reindeers]
        max_distance = 0
        max_index = []

        for (index, distance) in enumerate(distances):
            if distance > max_distance:
                max_distance = distance
                max_index = [index]
            elif distance == max_distance:
                max_index.append(index)

        for index in max_index:
            scores[index] += 1

    return scores


with open("input.txt", "r") as f:
    reindeers = f.readlines()

# part 1
print(max([find_distance(2503, *parse_line(line)) for line in reindeers]))

# part 2
print(max(new_score(2503, [parse_line(line) for line in reindeers])))

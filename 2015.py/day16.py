def parse_line(line: str) -> dict[str, int]:
    line = line.replace(":", "")
    line = line.replace(",", "")
    words = line.split()

    content = {}
    for i in range(2, len(words), 2):
        content[words[i]] = int(words[i + 1])

    return content


def judge_match(profile: dict, suspect: dict) -> bool:
    for item, count in suspect.items():
        if item in profile:
            # part 1
            # if count != profile[item]:
            #     return False

            # part 2
            if item == "cats" or item == "trees":
                if profile[item] >= count:
                    return False
            elif item == "pomeranians" or item == "goldfish":
                if profile[item] <= count:
                    return False
            else:
                if profile[item] != count:
                    return False

    return True


profile = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

with open("input16.txt", "r") as f:
    aunts = f.readlines()
    suspects = []

    for idx, aunt in enumerate(aunts):
        suspects.append((idx + 1, parse_line(aunt)))

    suspects = [i[0] for i in suspects if judge_match(profile, i[1])]

    print(suspects[0])

from string import ascii_lowercase as lowercase


def three_increasing(input: str) -> bool:
    return any(input[i : i + 3] in lowercase for i in range(len(input) - 3))


def avoid(input: str) -> bool:
    return all(i not in input for i in ["i", "o", "l"])


def two_pairs(input: str) -> bool:
    i = 1
    num_pairs = 0
    while i < len(input):
        if input[i] == input[i - 1]:
            num_pairs += 1
            i += 2
        else:
            i += 1

    return num_pairs >= 2


def increment(input: str) -> str:
    if input[-1] == "z":
        return increment(input[:-1]) + "a"
    next_letter = chr(ord(input[-1]) + 1)
    return input[:-1] + next_letter


# part 1
input = "cqjxjnds"

while True:
    input = increment(input)

    if avoid(input) and three_increasing(input) and two_pairs(input):
        break

print(input)

# part 2
while True:
    input = increment(input)

    if avoid(input) and three_increasing(input) and two_pairs(input):
        break

print(input)

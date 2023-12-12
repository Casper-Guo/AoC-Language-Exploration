from itertools import pairwise

vowels = ['a', 'e', 'i', 'o', 'u']
forbidden = ["ab", "cd", "pq", "xy"]


def three_vowels(input: str) -> bool:
    vowel_count = 0
    for char in input:
        if char in vowels:
            vowel_count += 1

    return vowel_count >= 3


def repeat_letter(input: str) -> bool:
    for i in range(len(input) - 1):
        if input[i] == input[i + 1]:
            return True

    return False


def separate_repeat(input: str) -> bool:
    for i in range(len(input) - 2):
        if input[i] == input[i + 2]:
            return True

    return False


def repeat_twice(input: str) -> bool:
    pairs = {}

    for idx, pair in enumerate(pairwise(input)):
        if pair in pairs:
            if pairs[pair] != idx - 1:
                return True
        else:
            pairs[pair] = idx

    return False


def no_forbidden(input: str) -> bool:
    return all([seq not in input for seq in forbidden])


with open("input05.txt", "r") as f:
    # part 1
    input = f.readlines()
    nice_count = 0

    for line in input:
        if three_vowels(line) and repeat_letter(line) and no_forbidden(line):
            nice_count += 1

    print(nice_count)

    # part 2
    nice_count = 0

    for line in input:
        if repeat_twice(line) and separate_repeat(line):
            nice_count += 1

    print(nice_count)

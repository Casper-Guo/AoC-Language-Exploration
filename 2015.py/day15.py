from math import prod

import utils

num_calls = 0


def parse_line(line: str) -> tuple[int]:
    line = line.strip().replace(",", "")

    # part 1
    # ignore calories
    # return tuple([int(i) for i in line.split() if utils.is_int(i)][:-1])

    # part 2
    return tuple([int(i) for i in line.split() if utils.is_int(i)])


def promising(remaining: int, properties: list[int], ingredients: list[tuple[int]]) -> bool:
    """
    Find whether the current combination is worth exploring further.

    Inputs:
        remaining - the number of remaining spaces / teaspoons
        properties - property values in the current combination
        ingredients - list of ingredient property values not yet considered

    Returns:
        Determine if the upper bound on any property value in the final combination is
        non-positive (not promising).
    """

    for idx, property in enumerate(properties):
        max_value = max([ingredient[idx] for ingredient in ingredients])

        if property + max_value * remaining <= 0:
            return False

    return True


def combinations(
    combination: list[int], remaining: int, properties: list[int], ingredients: list[tuple[int]]
) -> int:
    global num_calls
    num_calls += 1

    if remaining == 0:
        # base case

        # part 1
        # return prod([max(i, 0) for i in properties])

        # part 2
        if properties[-1] != 500:
            # doesn't meet calories requirements
            return 0
        return prod([max(i, 0) for i in properties[:-1]])

    if len(ingredients) == 1:
        # only one ingredient left
        # one step away from base case
        combination.append(remaining)
        ingredient = ingredients[0]

        for idx in range(len(properties)):
            properties[idx] += remaining * ingredient[idx]

        return combinations(combination, 0, properties, [])

    if not promising(remaining, properties, ingredients):
        # pruning
        return 0

    values = []
    ingredient = ingredients[0]

    for i in range(remaining + 1):
        new_combo = combination + [i]
        new_properties = []

        for idx in range(len(properties)):
            new_properties.append(properties[idx] + ingredient[idx] * i)

        values.append(combinations(new_combo, remaining - i, new_properties, ingredients[1:]))

    return max(values)


with open("input15.txt", "r") as f:
    input = f.readlines()

    # part 1 and 2 differences are in the implementations of the functions above

    ingredients = [parse_line(line) for line in input]
    num_properties = len(ingredients[0])

    print(combinations([], 100, [0] * num_properties, ingredients))
    print(num_calls)

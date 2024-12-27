from itertools import combinations
from math import prod

with open("input24.txt", "r") as f:
    weights = f.readlines()
    weights = [int(i.strip()) for i in weights]

    group_weight = sum(weights) // 3

    # part 1
    for i in range(5, len(weights)):
        quantum_entanglement = [
            prod(combo) for combo in combinations(weights, i) if sum(combo) == group_weight
        ]

        if quantum_entanglement:
            print(min(quantum_entanglement))
            break

    # part 2
    group_weight = sum(weights) // 4

    for i in range(4, len(weights)):
        quantum_entanglement = [
            prod(combo) for combo in combinations(weights, i) if sum(combo) == group_weight
        ]

        if quantum_entanglement:
            print(min(quantum_entanglement))
            break

from math import ceil
from itertools import combinations

boss_hp = 104
boss_dmg = 8
boss_armor = 1

weapons = [(8, 4, 0), (10, 5, 0), (25, 6, 0), (40, 7, 0), (74, 8, 0)]

armors = [(0, 0, 0), (13, 0, 1), (31, 0, 2), (53, 0, 3), (75, 0, 4), (102, 0, 5)]

rings = [
    (0, 0, 0),
    (0, 0, 0),
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
]


def judge_result(equipment: list) -> bool:
    """Judge if the boss can be beaten with the list of equipment."""
    player_dmg = sum([i[1] for i in equipment])
    player_armor = sum([i[2] for i in equipment])

    boss_turn = ceil(100 / max(1, boss_dmg - player_armor))
    player_turn = ceil(boss_hp / max(1, player_dmg - boss_armor))

    # player can beat the boss if the number of turns needed
    # is equal or less than boss_turn
    # return player_turn <= boss_turn

    # conversely, the player lost if the number of turns needed
    # is strictly greater than boss_turn
    return player_turn > boss_turn


# part 1
# min_spending = 500

# for weapon in weapons:
#     current_cost = weapon[0]

#     if current_cost >= min_spending:
#         continue

#     for armor in armors:
#         current_cost = weapon[0] + armor[0]

#         if current_cost >= min_spending:
#             continue

#         for ring1, ring2 in combinations(rings, 2):
#             current_cost = weapon[0] + armor[0] + ring1[0] + ring2[0]

#             if current_cost >= min_spending:
#                 continue

#             if judge_result([weapon, armor, ring1, ring2]):
#                 min_spending = current_cost

# print(min_spending)

# part 2
max_spending = 0

for weapon in weapons:
    current_cost = weapon[0]

    for armor in armors:
        current_cost = weapon[0] + armor[0]

        for ring1, ring2 in combinations(rings, 2):
            current_cost = weapon[0] + armor[0] + ring1[0] + ring2[0]

            if current_cost <= max_spending:
                continue

            if judge_result([weapon, armor, ring1, ring2]):
                max_spending = current_cost

print(max_spending)

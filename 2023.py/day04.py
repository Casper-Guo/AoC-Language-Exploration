import collections
import utils

def process_line(line) -> tuple[set, set]:
    cards = line.split('|')
    winning_numbers = set(utils.ints(cards[0])[1:])
    actual_numbers = set(utils.ints(cards[1]))

    return winning_numbers, actual_numbers


def calc_points(winning_numbers: set[int], actual_numbers: set[int]) -> float:
    num_winning = len([i for i in actual_numbers if i in winning_numbers])
    
    if num_winning:
        return 2 ** (num_winning - 1)
    else:
        return 0
    

def num_winning(winning_numbers: set[int], actual_numbers: set[int]) -> float:
    return len([i for i in actual_numbers if i in winning_numbers])


def main():
    with open("input4.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    lines = list(map(process_line, lines))

    # part 1
    print(sum(map(lambda x: calc_points(*x), lines)))

    # part 2
    num_cards = collections.defaultdict(lambda: 1)
    for i in range(len(lines)):
        num_cards[i + 1] = 1

    for idx, cards in enumerate(lines):
        card_idx = idx + 1
        points_won = num_winning(*cards)
        for i in range(card_idx + 1, card_idx + 1 + points_won):
            num_cards[i] += num_cards[card_idx]

    print(sum(val for key, val in num_cards.items() if key <= len(lines)))
    return

main()

from collections import Counter
from functools import total_ordering

CARD_STRENGTH = ['A', 'K', 'Q', 'J', 'T'] + [str(i) for i in range(9, 1, -1)]
CARD_STRENGTH = {card:i for i, card in enumerate(reversed(CARD_STRENGTH))}


@total_ordering
class Hand():
    def __init__(self, hand):
        self.hand = hand
        self.counter = Counter(hand)
        self.find_type()

    def is_five(self):
        return any([i == 5 for i in self.counter.values()])

    def is_four(self):
        return any([i == 4 for i in self.counter.values()])

    def is_full_house(self):
        return sorted(self.counter.values()) == [2, 3]
    
    def is_three(self):
        return any([i == 3 for i in self.counter.values()])

    def is_two(self):
        return list(self.counter.values()).count(2) == 2

    def is_one(self):
        return any([i == 2 for i in self.counter.values()])
    
    def part2_transform(self):
        if 'J' in self.counter:
            match self.type:
                case 0:
                    # high card becomes pair
                    self.type = 1
                case 1:
                    # pair becomes three
                    self.type = 3
                case 2:
                    # if J is not a pair then becomes full house
                    # else four of a kind
                    if self.counter['J'] == 1:
                        self.type = 4
                    elif self.counter['J'] == 2:
                        self.type = 5
                case 3:
                    # three becomes four
                    self.type = 5
                case 4:
                    # full house becomes five
                    self.type = 6
                case 5:
                    # four of a kind becomes five
                    self.type = 6
    
    def find_type(self):
        if self.is_five():
            self.type = 6
        elif self.is_four():
            self.type = 5
        elif self.is_full_house():
            self.type = 4
        elif self.is_three():
            self.type = 3
        elif self.is_two():
            self.type = 2
        elif self.is_one():
            self.type = 1
        else:
            self.type = 0

    def __eq__(self, other):
        return self.hand == other.hand
    
    def __lt__(self, other):
        if self.type != other.type:
            return self.type < other.type
        else:
            for self_card, other_card in zip(self.hand, other.hand):
                if CARD_STRENGTH[self_card] != CARD_STRENGTH[other_card]:
                    return CARD_STRENGTH[self_card] < CARD_STRENGTH[other_card]
            return False

    def __repr__(self):
        return f"{self.hand}, {self.type}"            


def process_line(line):
    line = line.split()
    return Hand(line[0]), int(line[1])


def main():
    with open("input7.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    lines = list(map(process_line, lines))

    # part 1
    winning = 0
    for idx, (hand, bid) in enumerate(sorted(lines, lambda x: x[0])):
        winning += (idx + 1) * bid
    
    print(winning)

    # part 2
    CARD_STRENGTH['J'] = -1
    for line in lines:
        line[0].part2_transform()
    
    winning = 0
    for idx, (hand, bid) in enumerate(sorted(lines, lambda x: x[0])):
        winning += (idx + 1) * bid
    
    print(winning)
    return

main()

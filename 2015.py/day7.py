from collections import deque
import time


class Instruction:
    def __init__(self, inputs: list[str], operation: str, output: str) -> None:
        self.inputs = inputs
        self.operation = operation
        self.output = output

    def __repr__(self):
        return f"{self.inputs} {self.operation} {self.output}"

    def check_inputs(self, signals: dict[str, int]) -> bool:
        return all([input in signals for input in self.inputs if not input.isdigit()])

    def find_output(self, signals: dict[str, int]) -> None:
        if self.operation == "NOT":
            output = ~signals[self.inputs[0]]
        elif self.operation == "->":
            if self.inputs[0].isdigit():
                output = int(self.inputs[0])
            else:
                # e.g lx -> a
                output = signals[self.inputs[0]]
        else:
            left, right = None, None
            if self.inputs[0].isdigit():
                left = int(self.inputs[0])
            else:
                left = signals[self.inputs[0]]

            if self.inputs[1].isdigit():
                right = int(self.inputs[1])
            else:
                right = signals[self.inputs[1]]

            if self.operation == "AND":
                output = left & right
            elif self.operation == "OR":
                output = left | right
            elif self.operation == "LSHIFT":
                output = left << right
            elif self.operation == "RSHIFT":
                output = left >> right

        # prevent overflow
        if output < 0:
            output = 65536 + output

        signals[self.output] = output


def parse_line(line: str) -> Instruction:
    words = line.split()

    if len(words) == 3:
        # straight forward pass from one wire to next
        return Instruction([words[0]], words[1], words[2])
    elif len(words) == 4:
        # Not operation
        return Instruction([words[1]], words[0], words[3])
    elif len(words) == 5:
        # all other operations
        return Instruction([words[0], words[2]], words[1], words[4])


with open("input7.txt", "r") as f:
    # part 1
    input = f.readlines()
    instructions = deque()
    signals = {}

    # input = ["123 -> x",
    #          "456 -> y",
    #          "x AND y -> d",
    #          "x OR y -> e",
    #          "x LSHIFT 2 -> f",
    #          "y RSHIFT 2 -> g",
    #          "NOT x -> h",
    #          "NOT y -> i"]

    # for line in input:
    #     instructions.append(parse_line(line))

    # while instructions:
    #     new_instruction = instructions.popleft()

    #     if new_instruction.check_inputs(signals):
    #         new_instruction.find_output(signals)
    #     else:
    #         instructions.append(new_instruction)

    # print(signals['a'])

    # part 2
    # required a hack by modifying the input
    # change the instruction 1674 -> b to 46065 -> b
    # not sure why that made the difference
    for line in input:
        instructions.append(parse_line(line))

    while instructions:
        new_instruction = instructions.popleft()

        if new_instruction.check_inputs(signals):
            new_instruction.find_output(signals)
        else:
            instructions.append(new_instruction)

    print(signals['a'])

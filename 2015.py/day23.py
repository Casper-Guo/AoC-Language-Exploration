def parse_line(line: str) -> list[str]:
    return line.strip().replace(",", "").split()


def execute_instruction(
    reg_a: int, reg_b: int, instructions: list[list[str]], index: int
) -> tuple[int, int, int]:
    instruction = instructions[index]

    if instruction[0] == "hlf":
        if instruction[1] == "a":
            reg_a /= 2
        else:
            reg_b /= 2
        return reg_a, reg_b, index + 1
    elif instruction[0] == "tpl":
        if instruction[1] == "a":
            reg_a *= 3
        else:
            reg_b *= 3
        return reg_a, reg_b, index + 1
    elif instruction[0] == "inc":
        if instruction[1] == "a":
            reg_a += 1
        else:
            reg_b += 1
        return reg_a, reg_b, index + 1
    elif instruction[0] == "jmp":
        return reg_a, reg_b, index + int(instruction[1])
    elif instruction[0] == "jie":
        if instruction[1] == "a":
            if reg_a % 2 == 0:
                return reg_a, reg_b, index + int(instruction[2])
            else:
                return reg_a, reg_b, index + 1
        else:
            if reg_b % 2 == 0:
                return reg_a, reg_b, index + int(instruction[2])
            else:
                return reg_a, reg_b, index + 1
    elif instruction[0] == "jio":
        if instruction[1] == "a":
            if reg_a == 1:
                return reg_a, reg_b, index + int(instruction[2])
            else:
                return reg_a, reg_b, index + 1
        else:
            if reg_b == 1:
                return reg_a, reg_b, index + int(instruction[2])
            else:
                return reg_a, reg_b, index + 1


with open("input23.txt", "r") as f:
    input = f.readlines()

    instructions = [parse_line(line) for line in input]
    index = 0
    reg_a = 1
    reg_b = 0

    while index < len(instructions):
        print(instructions[index], reg_a, reg_b)
        reg_a, reg_b, index = execute_instruction(reg_a, reg_b, instructions, index)

    print(reg_b)

def count_char(line: str) -> int:
    i = 0
    count = 0
    while i < len(line):
        if line[i] == "\\":
            if line[i + 1] == '"' and i != len(line) - 2:
                # \" escape sequence
                count += 1
                i += 2
            elif line[i + 1] == "\\":
                # \\ escape sequence
                count += 1
                i += 2
            elif line[i + 1] == "x":
                # ASCII escape sequence
                count += 1
                i += 4
            else:
                # not an escape sequence
                count += 1
                i += 1
        else:
            count += 1
            i += 1

    # ignores the enclosing double quotes
    return count - 2


def translate(line: str) -> int:
    # the two enclosing double quotes increase the length by 4
    # each \" sequence becomes \\\"
    # each \x sequence becomes \\x

    return (line.count(r'"') - 2) + 4 + line.count("\\")


with open("input08.txt", "r") as f:
    # part 1
    input = f.readlines()
    input = [line.strip() for line in input]

    # input = [r'""', r'"abc"', r'"aaa\"aaa"', r'"\x27"']

    sum = 0
    for line in input:
        sum += len(line) - count_char(line)

    print(sum)

    # part 2
    sum = 0
    for line in input:
        sum += translate(line)

    print(sum)

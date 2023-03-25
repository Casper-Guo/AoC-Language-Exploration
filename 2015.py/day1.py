with open('input1.txt', 'r') as f:
    # part 1
    input = f.read()
    print(input.count("(") - input.count(")"))

    # part 2
    floor = 0
    for (idx, char) in enumerate(input):
        if char == '(':
            floor += 1
        else:
            floor -= 1
        if floor == -1:
            print(idx + 1)
            break

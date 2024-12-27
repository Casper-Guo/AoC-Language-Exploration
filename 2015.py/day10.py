def transform_string(input: list[str]) -> list[str]:
    if len(input) == 1:
        return input * 2

    output = []

    # move pointer to first position
    i = 1
    digit = input[0]
    count = 1

    while i < len(input):
        if digit == input[i]:
            count += 1
        else:
            output.append(str(count))
            output.append(digit)
            digit = input[i]
            count = 1
        i += 1

    output.append(str(count))
    output.append(digit)
    return output


input = list("1321131112")

# part 1
for _ in range(40):
    input = transform_string(input)

print(len(input))

# part 2
for _ in range(10):
    input = transform_string(input)

print(len(input))

def translate_move(char: str) -> tuple[int, int]:
    if char == '^':
        return (0, 1)
    elif char == "v":
        return (0, -1)
    elif char == "<":
        return (-1, 0)
    elif char == ">":
        return (1, 0)
    else:
        return (0, 0)


with open("input03.txt", "r") as f:
    # part one
    input = f.read()
    visited = {(0, 0)}
    current_x = 0
    current_y = 0

    for char in input:
        x_move, y_move = translate_move(char)
        current_x += x_move
        current_y += y_move
        visited.add((current_x, current_y))

    print(len(visited))

    # part two
    visited = {(0, 0)}

    santa_x = 0
    santa_y = 0
    robot_x = 0
    robot_y = 0

    for idx, char in enumerate(input):
        x_move, y_move = translate_move(char)
        if idx % 2 == 0:
            # santa move
            santa_x += x_move
            santa_y += y_move
            visited.add((santa_x, santa_y))
        else:
            robot_x += x_move
            robot_y += y_move
            visited.add((robot_x, robot_y))

    print(len(visited))

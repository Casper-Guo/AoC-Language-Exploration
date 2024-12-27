from utils import ARROWS_TO_DELTA

with open("input03.txt", "r") as f:
    # part one
    input = f.read()
    visited = {(0, 0)}
    current_row = 0
    current_col = 0

    for char in input:
        drow, dcol = ARROWS_TO_DELTA[char]
        current_row += drow
        current_col += dcol
        visited.add((current_row, current_col))

    print(len(visited))

    # part two
    visited = {(0, 0)}

    santa_row = 0
    santa_col = 0
    robot_row = 0
    robot_col = 0

    for idx, char in enumerate(input):
        drow, dcol = ARROWS_TO_DELTA[char]
        if idx % 2 == 0:
            # santa move
            santa_row += drow
            santa_col += dcol
            visited.add((santa_row, santa_col))
        else:
            robot_row += drow
            robot_col += dcol
            visited.add((robot_row, robot_col))

    print(len(visited))

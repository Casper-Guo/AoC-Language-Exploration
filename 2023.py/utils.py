'''Source: https://github.com/mcpower/adventofcode/blob/master/utils.py#L12'''

import re

def lmap(func, *iterables):
    return list(map(func, *iterables))

# string processing
def ints(s: str) -> list[int]:
    assert isinstance(s, str), f"you passed in a {type(s)}!!!"
    return lmap(int, re.findall(r"(?:(?<!\d)-)?\d+", s))  # thanks mserrano!


def positive_ints(s: str) -> list[int]:
    assert isinstance(s, str), f"you passed in a {type(s)}!!!"
    return lmap(int, re.findall(r"\d+", s))  # thanks mserrano!


def floats(s: str) -> list[float]:
    assert isinstance(s, str), f"you passed in a {type(s)}!!!"
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def positive_floats(s: str) -> list[float]:
    assert isinstance(s, str), f"you passed in a {type(s)}!!!"
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))


def words(s: str) -> list[str]:
    assert isinstance(s, str), f"you passed in a {type(s)}!!!"
    return re.findall(r"[a-zA-Z]+", s)


# Grid movement constants
GRID_DELTA = [[-1, 0], [1, 0], [0, -1], [0, 1]]
OCT_DELTA = [[1, 1], [-1, -1], [1, -1], [-1, 1]] + GRID_DELTA
CHAR_TO_DELTA = {
    "U": [-1, 0],
    "R": [0, 1],
    "D": [1, 0],
    "L": [0, -1],
    "N": [-1, 0],
    "E": [0, 1],
    "S": [1, 0],
    "W": [0, -1],
}
DELTA_TO_UDLR = {
    (-1, 0): "U",
    (0, 1): "R",
    (1, 0): "D",
    (0, -1): "L",
}
DELTA_TO_NESW = {
    (-1, 0): "N",
    (0, 1): "E",
    (1, 0): "S",
    (0, -1): "W",
}

# Grid movement functions
def turn_180(drowcol:tuple[int, int]) -> tuple[int, int]:
    drow, dcol = drowcol
    return -drow, -dcol


def turn_right(drowcol:tuple[int, int]) -> tuple[int, int]:
    # positive dcol -> positive drow
    # positive drow -> negative dcol
    drow, dcol = drowcol
    return dcol, -drow


def turn_left(drowcol:tuple[int, int]) -> tuple[int, int]:
    drow, dcol = drowcol
    return [-dcol, drow]


def print_grid(grid):
    for line in grid:
        print(*line, sep="")
    return

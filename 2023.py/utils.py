'''Source: https://github.com/mcpower/adventofcode/blob/master/utils.py#L12'''

import re
from typing import Iterable, Generic, TypeVar, Self, TypeAlias
from collections import defaultdict

Coord: TypeAlias = tuple[int, int]
Direction: TypeAlias = tuple[int, int]
Node: TypeAlias = tuple[Coord, Direction]

T = TypeVar('T')

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


# built-in enhancements
def list_split(original: list, sep) -> list[list]:
    """Split a list into list at lists by the value sep."""
    splits = []
    split = []

    for i in original:
        if i != sep:
            split.append(i)
        else:
            splits.append(split)
            split = []
    
    if split:
        splits.append(split)

    return splits


def dict_transpose(dictionary: dict) -> dict:
    new_dict = defaultdict(set)

    for key, value in dictionary.items():
        if isinstance(value, Iterable):
            for val in value:
                new_dict[val].add(key)
        else:
            new_dict[value].add(key)

    return dict(new_dict)


class Grid(Generic[T]):
    """2D grid."""

    def __init__(self, grid: Iterable[Iterable[T]]) -> None:
        self.grid = grid
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.shape = (self.rows, self.cols)
    
    def coords(self) -> list[Coord]:
        return [(r, c) for r in range(self.rows) for c in range(self.cols)]
    
    def get_row(self, row: int) -> Iterable[T]:
        return self.grid[row]
    
    def get_col(self, col: int) -> list[T]:
        return [self[i, col] for i in range(self.rows)]
    
    def check_inbound(self, coord: Iterable[int]) -> bool:
        row, col = coord[0], coord[1]
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def get_dir_neighbors(self, coord: Iterable[int]) -> list[Coord]:
        neighbors = []
        row, col = coord[0], coord[1]
        for delta_row, delta_col in GRID_DELTA:
            neighbor = (row + delta_row, col + delta_col)
            if self.check_inbound(neighbor):
                neighbors.append(neighbor)
        return neighbors
    
    def get_adj_neighbors(self, coord: Iterable[int]) -> list[Coord]:
        neighbors = []
        row, col = coord[0], coord[1]
        for delta_row, delta_col in OCT_DELTA:
            neighbor = (row + delta_row, col + delta_col)
            if self.check_inbound(neighbor):
                neighbors.append(neighbor)
        return neighbors
    
    def find(self, target: T) -> list[Coord]:
        return [coord for coord in self.coords() if self[coord] == target]
    
    def transpose(self):
        new_grid = [self.get_col(i) for i in range(self.cols)]
        self.grid = new_grid

    def reflec_y(self):
        """Vertical reflection.
        
        1 2
        3 4

        becomes

        2 1
        4 3        
        """
        new_grid = [reversed(self.get_row(i)) for i in range(self.rows)]
        self.grid = new_grid

    def reflect_x(self):
        """Horizontal reflection.
        
        1 2
        3 4

        becomes

        3 4
        1 2
        """
        new_grid = [self.get_row(i) for i in range(self.rows - 1, -1, -1)]
        self.grid = new_grid

    def rotate_left_90(self):
        """
        1 2
        3 4

        becomes

        2 4
        1 3
        """
        new_grid = [self.get_col(i) for i in range(self.cols - 1, -1, -1)]
        self.grid = new_grid

    def rotate_right_90(self):
        """
        1 2
        3 4

        becomes
        
        3 1
        4 2
        """
        new_grid = [reversed(self.get_col(i)) for i in range(self.cols)]
        self.grid = new_grid

    def __add__(self, other: Self) -> Self:
        assert self.shape == other.shape, f"Shape mismatch: {self.shape}, {other.shape}"

        sum_grid = Grid([[0] * self.cols] * self.rows)

        for coord in self.coords:
            sum_grid[coord] = self[coord] + other[coord]

        return sum_grid
    
    def __sub__(self, other: Self) -> Self:
        assert self.shape == other.shape, f"Shape mismatch: {self.shape}, {other.shape}"

        diff_grid = Grid([[0] * self.cols] * self.rows)

        for coord in self.coords:
            diff_grid[coord] = self[coord] - other[coord]

        return diff_grid
    
    def __contains__(self, coord: Iterable[int]) -> bool:
        return self.check_inbound(coord)
    
    def __eq__(self, other):
        """Two grids are equal if all elements are equal."""
        if self.rows != other.rows or self.cols != other.cols:
            return False
        else:
            for coord in self.coords():
                if self[coord] != other[coord]:
                    return False
        return True
    
    def __getitem__(self, coord: Iterable[int]) -> T:
        return self.grid[coord[0]][coord[1]]
    
    def __setitem__(self, coord: Iterable[int], value: T):
        self.grid[coord[0]][coord[1]] = value
    
    def __repr__(self):
        ret = ''
        for i in range(self.rows):
            ret += str(self.get_row(i)) + '\n'
        return ret


# Grid movement constants
GRID_DELTA = [(1, 0), (-1, 0), (0, 1), (0, -1)]
OCT_DELTA = [(1, 1), (-1, -1), (1, -1), (-1, 1)] + GRID_DELTA
CHAR_TO_DELTA = {
    "U": (-1, 0),
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
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

def change_direction(current_coord: Coord, direction: Direction) -> Node:
    return (current_coord[0] + direction[0], current_coord[1] + direction[1]), direction


def get_direction(current: Coord, prev: Coord) -> Direction:
    return current[0] - prev[0], current[1] - prev[1]


# Grid movement functions
def turn_180(drowcol:Direction) -> Direction:
    drow, dcol = drowcol
    return -drow, -dcol


def turn_right(drowcol:Direction) -> Direction:
    # positive dcol -> positive drow
    # positive drow -> negative dcol
    drow, dcol = drowcol
    return dcol, -drow


def turn_left(drowcol:Direction) -> Direction:
    drow, dcol = drowcol
    return -dcol, drow


def print_grid(grid):
    for line in grid:
        print(*line, sep="")
    return

# MISC
DIGITS = {'zero':0, 'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9}

def find_iter(x: int, y: int) -> int:
    """This coordinate is the ?th number to be generated."""
    # this is the ?th diagonal to be generated
    diagonal_num = x + y - 1

    # number of grids in the previous diagonals
    # 1 + 2 ... + (diagonal_num - 1)
    num_previous = diagonal_num * (diagonal_num - 1) // 2

    # number of grids in the current diagonal
    # before (x, y)
    num_previous += diagonal_num - y + 1

    return num_previous


def find_grid(x: int, y: int) -> int:
    # xth number to be generated
    # implies x-1 iterations from seed
    num_iter = find_iter(x, y) - 1

    seed = 20151125
    factor = 252533
    modular = 33554393

    for i in range(num_iter):
        seed = (seed * factor) % modular

    return seed

# part 1
print(find_grid(3075, 2981))
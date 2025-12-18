import itertools

import utils
import z3


def process_line(line: str) -> tuple[int, ...]:
    return tuple(utils.ints(line))


def find_intersection(
    stone1: tuple[int, ...], stone2: tuple[int, ...]
) -> tuple[float | None, float | None]:
    x_1, y_1, _, v_x1, v_y1, _ = stone1
    x_2, y_2, _, v_x2, v_y2, _ = stone2

    if v_x1 * v_y2 == v_y1 * v_x2:
        # the two paths are parallel
        return None, None

    m_1 = v_y1 / v_x1
    m_2 = v_y2 / v_x2
    b_1 = y_1 - m_1 * x_1
    b_2 = y_2 - m_2 * x_2

    # solve
    # y = m_1 * x + b_1
    # y = m_2 * x + b_2
    x = (b_2 - b_1) / (m_1 - m_2)
    y = m_1 * x + b_1

    t_1 = (x - x_1) / (v_x1)
    t_2 = (x - x_2) / (v_x2)

    if t_1 < 0 or t_2 < 0:
        return None, None

    return x, y


def solve_init(stones: list[tuple[int, ...]]) -> tuple[int, int, int]:
    s = z3.Solver()
    x_0, y_0, z_0 = z3.Int("x_0"), z3.Int("y_0"), z3.Int("z_0")
    v_x0, v_y0, v_z0 = z3.Int("v_x0"), z3.Int("v_y0"), z3.Int("v_z0")

    for i, stone in enumerate(stones):
        x, y, z, v_x, v_y, v_z = stone
        t = z3.Int(f"t_{i + 1}")
        s.add(t >= 0)
        s.add(x_0 + v_x0 * t == x + v_x * t)
        s.add(y_0 + v_y0 * t == y + v_y * t)
        s.add(z_0 + v_z0 * t == z + v_z * t)

    s.check()
    m = s.model()
    return m[x_0].as_long(), m[y_0].as_long(), m[z_0].as_long()


def main() -> None:
    with open("input24.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    stones = list(map(process_line, lines))

    test_area_intersect = 0
    lims = (200000000000000, 400000000000000)

    for stone1, stone2 in itertools.combinations(stones, r=2):
        x, y = find_intersection(stone1, stone2)
        if x is not None and lims[0] <= x <= lims[1] and lims[0] <= y <= lims[1]:
            test_area_intersect += 1

    print(test_area_intersect)
    print(sum(solve_init(stones)))


if __name__ == "__main__":
    main()

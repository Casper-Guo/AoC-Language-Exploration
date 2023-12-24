import itertools
import utils

def process_line(line):
    return tuple(utils.ints(line))


def find_intersection(stone1, stone2):
    x_1, y_1, z_1, v_x1, v_y1, v_z1 = stone1
    x_2, y_2, z_2, v_x2, v_y2, v_z2 = stone2
    
    m_1 = v_y1 / v_x1
    m_2 = v_y2 / v_x2

    if abs(m_1 - m_2) < 0.0001:
        return None, None
    
    b_1 = y_1 - m_1 * x_1
    b_2 = y_2 - m_2 * x_2

    x = (b_2 - b_1) / (m_1 - m_2)
    y = m_1 * x + b_1

    t_1 = (x - x_1) / (v_x1)
    t_2 = (x - x_2) / (v_x2)

    if t_1 < 0 or t_2 < 0:
        return None, None
    
    return x, y


def main():
    with open("input24.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    stones = list(map(process_line, lines))

    test_area_intersect = 0
    lims = (200000000000000, 400000000000000)

    for stone1, stone2 in itertools.combinations(stones, r=2):
        x, y = find_intersection(stone1, stone2)
        if x is not None:
            if lims[0] <= x <= lims[1] and lims[0] <= y <= lims[1]:
                test_area_intersect += 1

    print(test_area_intersect)
    return

main()

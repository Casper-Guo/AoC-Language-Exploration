import utils
from math import prod, ceil, floor
from scipy.optimize import fsolve

def simulate(time: int, distance: int, hold: int):
    return (time - hold) * hold > distance

def main():
    with open("input6.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    
    times, distances = utils.ints(lines[0]), utils.ints(lines[1])

    # part 1
    ways_to_win = [len([i for i in range(time) if simulate(time, distance, i)]) for time, distance in zip(times, distances)]    
    print(prod(ways_to_win))

    new_time = utils.ints(lines[0].replace(' ', ''))[0]
    new_distance = utils.ints(lines[1].replace(' ', ''))[0]

    # part 2 brute force
    # print(len(list(i for i in range(new_time) if simulate(new_time, new_distance, i))))

    # part 2 math
    roots = fsolve(lambda x: x * new_time - x ** 2 - new_distance, x0=[0, new_distance])
    print(floor(roots[1]) - ceil(roots[0]) + 1)
    return

main()

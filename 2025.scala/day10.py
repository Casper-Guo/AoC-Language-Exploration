from itertools import starmap
from pathlib import Path

import pulp


def process_line(line: str) -> tuple[list[set[int]], list[int]]:
    # trim the light diagram
    line = line[line.find("]") + 1 :]
    buttons = [
        {int(j) for j in i.strip("()").split(",")} for i in line[: line.rfind(" ")].split()
    ]
    joltages = [int(i) for i in line[line.rfind(" ") + 1 :].strip("{}").split(",")]
    return buttons, joltages


def min_presses(buttons: list[set[int]], joltages: list[int]) -> int:
    problem = pulp.LpProblem("min_presses", pulp.LpMinimize)
    vars = [pulp.LpVariable(f"b{i}", lowBound=0, cat="Integer") for i in range(len(buttons))]
    problem += pulp.lpSum(vars)
    for counter, target in enumerate(joltages):
        problem += (
            pulp.lpSum(
                vars[i] * (1 if counter in button_set else 0)
                for i, button_set in enumerate(buttons)
            )
            == target
        )
    problem.solve(pulp.PULP_CBC_CMD(msg=False))
    return int(pulp.value(problem.objective))


def main() -> None:
    text = Path("input10.txt").read_text().strip().split("\n")
    inputs = [process_line(line) for line in text]
    print(sum(starmap(min_presses, inputs)))


if __name__ == "__main__":
    main()

import regex as re
import utils
from math import prod


def process_instructions(instructions):
    instructions = instructions.split(",")

    for idx, instruction in enumerate(instructions[:-1]):
        captures = re.search(r"(\w{1})([<>]{1})(\d+):(\w+)", instruction)
        captures = list(captures.groups())
        captures[1] = captures[1] == "<"
        captures[2] = int(captures[2])
        instructions[idx] = tuple(captures)

    return tuple(instructions)


def process_workflows(workflows):
    processed_workflows = {}
    for workflow in workflows:
        captures = re.search(r"(\w+)\{(.+)\}", workflow)
        name, instructions = captures.groups()
        processed_workflows[name] = process_instructions(instructions)

    return processed_workflows


def process_part(part):
    part = utils.ints(part)
    return {category: rating for category, rating in zip(["x", "m", "a", "s"], part)}


def run_one_workflow(workflow: list, part: dict[str, int]) -> str:
    for step in workflow[:-1]:
        category, predicate, comp_value, next_workflow = step

        if predicate:
            # less than comparison
            if part[category] < comp_value:
                return next_workflow
        else:
            # greater than comparison
            if part[category] > comp_value:
                return next_workflow

    return workflow[-1]


def check_accept(workflows: dict[str, list], part: dict[str, int]) -> int:
    """Return 1 if accepted, return 0 if rejected."""
    current_workflow = "in"

    while current_workflow not in ["A", "R"]:
        current_workflow = run_one_workflow(workflows[current_workflow], part)

    return int(current_workflow == "A")


def make_hashable(sets: list[set]) -> tuple[tuple[int]]:
    return tuple(map(tuple, sets))


def make_set(ranges: list[set]) -> set[tuple[tuple[int]]]:
    return set([make_hashable(ranges)])


CATEGORY_TO_INDEX = {"x": 0, "m": 1, "a": 2, "s": 3}


def find_accept_ranges(
    workflows: dict[str, list], workflow: list, accept_ranges: set[tuple[range]]
):
    if workflow == "A":
        return accept_ranges
    if workflow == "R":
        return set()

    workflow_ranges = set()
    for accept_range in accept_ranges:
        accept_range = list(accept_range)

        for step in workflow[:-1]:
            category, predicate, comp_value, next_workflow = step
            category = CATEGORY_TO_INDEX[category]
            next_workflow = workflows.get(next_workflow, next_workflow)

            remove = set()
            if predicate:
                remove = set(filter(lambda x: x < comp_value, accept_range[category]))
            else:
                remove = set(filter(lambda x: x > comp_value, accept_range[category]))

            temp = accept_range[category]
            accept_range[category] = remove
            workflow_ranges.update(
                find_accept_ranges(workflows, next_workflow, make_set(accept_range))
            )
            accept_range[category] = set(filter(lambda x: x not in remove, temp))

        next_workflow = workflows.get(workflow[-1], workflow[-1])
        workflow_ranges.update(
            find_accept_ranges(workflows, next_workflow, make_set(accept_range))
        )

    return workflow_ranges


def main():
    with open("input19.txt", "r") as f:
        text = f.read().split("\n\n")
        workflows, parts = text[0], text[1]
        workflows = list(map(lambda x: x.strip(), workflows.split("\n")))
        parts = list(map(lambda x: x.strip(), parts.split("\n")))

    workflows = process_workflows(workflows)
    parts = list(map(process_part, parts))

    # part 1
    accepted_sum = 0
    for part in parts:
        accepted_sum += check_accept(workflows, part) * sum(part.values())
    print(accepted_sum)

    # part 2
    accept_ranges = set()
    accept_ranges.add(make_hashable([set(range(1, 4001))] * 4))

    accept_ranges = find_accept_ranges(workflows, workflows["in"], accept_ranges)
    print(sum(prod(len(i) for i in ranges) for ranges in accept_ranges))
    return


main()

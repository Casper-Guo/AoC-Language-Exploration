import json


def json_sum(object: dict | list | str | int) -> int:
    if isinstance(object, int):
        return object
    if isinstance(object, str):
        return 0
    if isinstance(object, list):
        return sum([json_sum(i) for i in object])
    if isinstance(object, dict):
        # part 1
        # return sum([json_sum(i) for i in object.values()])

        # part 2
        if "red" not in object.values():
            return sum([json_sum(i) for i in object.values()])
        return 0
    return 0


with open("input12.txt", "r") as f:
    input = json.load(f)
    print(json_sum(input))

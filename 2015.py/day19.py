import re


def parse_line(line: str) -> tuple[str, str]:
    words = line.strip().split()

    return words[0], words[-1]


def one_replacement(
    molecule: str, original: str, replacement: str, all_molecules: set[str]
) -> None:
    """
    Replace all substrings matching original in molecule one by one with replacement.

    Add all new molecules to all_molecules.
    """
    for m in re.finditer(original, molecule):
        new_string = molecule[: m.start()] + replacement + molecule[m.end() :]
        all_molecules.add(new_string)


with open("input19.txt", "r") as f:
    input = f.readlines()
    molecule = input[-1].strip()
    replacements = []

    for line in input[:-2]:
        replacements.append(parse_line(line))

    # part 1
    unique_molecules = set()

    for original, replacement in replacements:
        one_replacement(molecule, original, replacement, unique_molecules)

    print(len(unique_molecules))

    # part 2
    # greedy approach doesn't work
    # recursive enumeration?

    # Solved with Reddit formula, for now

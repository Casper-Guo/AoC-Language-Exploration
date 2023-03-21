def paper_needed(dim1, dim2, dim3):
    face1 = dim1 * dim2
    face2 = dim2 * dim3
    face3 = dim1 * dim3

    return 2 * (face1 + face2 + face3) + min(face1, face2, face3)


def ribbon_needed(dim1, dim2, dim3):
    per1 = 2 * (dim1 + dim2)
    per2 = 2 * (dim1 + dim3)
    per3 = 2 * (dim2 + dim3)

    return min(per1, per2, per3) + dim1 * dim2 * dim3


def parse_line(line):
    return (int(i) for i in line.split("x"))


with open("input.txt", "r") as f:
    # part 1
    input = f.readlines()
    total_paper = 0
    for line in input:
        total_paper += paper_needed(*parse_line(line))
    print(total_paper)

    # part 2
    total_ribbon = 0
    for line in input:
        total_ribbon += ribbon_needed(*parse_line(line))
    print(total_ribbon)

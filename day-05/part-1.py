import numpy as np
from os import path


def read_file(name: str) -> tuple[list[int], list[np.array]]:
    with open(name) as f:
        content = f.read().split("\n")

    lines = []
    for line in content:
        c1, c2 = line.split(" -> ")
        s1, s2 = c1.split(",")
        d1, d2 = c2.split(",")

        lines.append([[int(s1), int(s2)], [int(d1), int(d2)]])

    return np.array(lines)


def generate_mask(line: np.array, width: int, height: int) -> np.array:
    src, dst = line
    field = np.zeros((width, height), dtype=bool)

    min_x, max_x = min(src[0], dst[0]), max(src[0], dst[0])
    min_y, max_y = min(src[1], dst[1]), max(src[1], dst[1])

    if src[0] == dst[0]:
        field[src[0], min_y : max_y + 1] = True
    elif src[1] == dst[1]:
        field[min_x : max_x + 1, src[1]] = True
    else:
        # This is the diagonal case.
        pass

    return field


def map_danger_zones(lines: np.array) -> int:
    width = lines[:, :, 0].max() + 1
    height = lines[:, :, 1].max() + 1

    field = np.zeros((width, height), dtype=int)

    for line in lines:
        np.putmask(field, generate_mask(line, width, height), field + 1)

    return np.count_nonzero(field > 1)


lines = read_file(path.join(path.dirname(__file__), "./input-1.txt"))

danger_zones_count = map_danger_zones(lines)
assert danger_zones_count == 5

lines = read_file(path.join(path.dirname(__file__), "./input-2.txt"))

danger_zones_count = map_danger_zones(lines)
print(danger_zones_count)

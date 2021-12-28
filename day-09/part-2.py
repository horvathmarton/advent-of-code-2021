from os import path
from math import prod


def read_file(name: str) -> list[int]:
    with open(name) as f:
        lines = []
        for line in f.read().split("\n"):
            lines.append([[int(digit), False] for digit in list(line)])

        return lines


def get_neighbors(heights: list[list[int]], x: int, y: int) -> dict[str, int]:
    result = {}

    if y > 0:
        result["top"] = heights[y - 1][x]

    if y < len(heights) - 1:
        result["bottom"] = heights[y + 1][x]

    if x > 0:
        result["left"] = heights[y][x - 1]

    if x < len(heights[0]) - 1:
        result["right"] = heights[y][x + 1]

    return result


def unmark_visited(
    heights: list[list[tuple[int, bool]]]
) -> list[list[tuple[int, bool]]]:
    for line in heights:
        for item in line:
            item[1] = False


def get_basin_size(heights: list[list[int]], x: int, y: int) -> int:
    heights[y][x][1] = True
    neighs = get_neighbors(heights, x, y)

    if all([n[0] == 9 or n[1] for n in neighs.values()]):
        return 1

    result = 1
    if "top" in neighs and not neighs["top"][1] and neighs["top"][0] != 9:
        result += get_basin_size(heights, x, y - 1)
    if "bottom" in neighs and not neighs["bottom"][1] and neighs["bottom"][0] != 9:
        result += get_basin_size(heights, x, y + 1)
    if "left" in neighs and not neighs["left"][1] and neighs["left"][0] != 9:
        result += get_basin_size(heights, x - 1, y)
    if "right" in neighs and not neighs["right"][1] and neighs["right"][0] != 9:
        result += get_basin_size(heights, x + 1, y)

    return result


def find_local_minimums(heights: list[list[int]]) -> list[int]:
    result = []

    for y, _ in enumerate(heights):
        for x, _ in enumerate(heights[0]):
            item = heights[y][x]
            neigh = get_neighbors(heights, x, y)

            if all((item[0] < n[0] for n in neigh.values())):
                unmark_visited(heights)
                result.append(get_basin_size(heights, x, y))

    return sorted(result, reverse=True)


heights = read_file(path.join(path.dirname(__file__), "./input-1.txt"))

basin_sizes = find_local_minimums(heights)
assert prod(basin_sizes[:3]) == 1134

heights = read_file(path.join(path.dirname(__file__), "./input-2.txt"))

basin_sizes = find_local_minimums(heights)
print(prod(basin_sizes[:3]))

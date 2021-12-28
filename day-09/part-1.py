from os import path


def read_file(name: str) -> list[int]:
    with open(name) as f:
        lines = []
        for line in f.read().split("\n"):
            lines.append([int(digit) for digit in list(line)])

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


def find_local_minimums(heights: list[list[int]]) -> list[int]:
    result = []

    for y, _ in enumerate(heights):
        for x, _ in enumerate(heights[0]):
            item = heights[y][x]
            neigh = get_neighbors(heights, x, y)

            if all((item < n for n in neigh.values())):
                result.append(item)

    return result


heights = read_file(path.join(path.dirname(__file__), "./input-1.txt"))

mins = find_local_minimums(heights)
assert sum(mins) + len(mins) == 15

heights = read_file(path.join(path.dirname(__file__), "./input-2.txt"))

mins = find_local_minimums(heights)
print(sum(mins) + len(mins))

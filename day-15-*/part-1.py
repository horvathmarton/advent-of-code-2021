from os import path
import numpy as np
import heapq


def read_file(name: str) -> np.array:
    with open(name) as f:
        lines = []
        for line in f.read().split("\n"):
            lines.append([int(num) for num in list(line)])

        return np.array(lines)


def next_point(x: int, y: int, shape: tuple[int, int]):
    if x < shape[0] - 1:
        yield x + 1, y

    if y < shape[1] - 1:
        yield x, y + 1


def find_shortest_path(matrix: np.array) -> int:
    costs = np.zeros(matrix.shape)
    to_process = [(0, (0, 0))]
    counter = 0

    while to_process:
        cost, coord = heapq.heappop(to_process)
        x, y = coord

        if counter % 1_000_000 == 0:
            print(
                f"Queue size: {len(to_process)}, Current coordinate: {coord}, Position weight: {x + y}"
            )

        if costs[x, y] == 0 or cost < costs[x, y]:
            costs[x, y] = cost

        if coord == (matrix.shape[0] - 1, matrix.shape[1] - 1):
            return cost

        for x, y in next_point(*coord, matrix.shape):
            new_cost = cost + matrix[x, y]
            if costs[x, y] == 0 or new_cost < costs[x, y]:
                heapq.heappush(to_process, (new_cost, (x, y)))

        counter += 1

    return costs[matrix.shape[0] - 1, matrix.shape[1] - 1]


matrix = read_file(path.join(path.dirname(__file__), "./input-1.txt"))
shortest_path = find_shortest_path(matrix)
print(shortest_path)
assert shortest_path == 40

matrix = read_file(path.join(path.dirname(__file__), "./input-2.txt"))
shortest_path = find_shortest_path(matrix)
print(shortest_path)

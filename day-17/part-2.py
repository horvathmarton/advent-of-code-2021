from os import path
from re import findall
from itertools import product


def read_file(name: str) -> str:
    with open(name) as f:
        params = findall(r"x=(-?\d*..-?\d*), y=(-?\d*..-?\d*)", f.read())

    x1, x2 = params[0][0].split("..")
    y1, y2 = params[0][1].split("..")

    return ((int(x1), int(x2)), (int(y1), int(y2)))


def simulate_aim(
    x: tuple[int, int], y: tuple[int, int], starting_speed: tuple[int, int]
) -> bool:
    position = (0, 0)
    speed = starting_speed

    while position[0] <= max(x) and position[1] >= min(y):
        position = (position[0] + speed[0], position[1] + speed[1])
        speed = (max(0, speed[0] - 1), speed[1] - 1)

        if x[0] <= position[0] <= x[1] and y[0] <= position[1] <= y[1]:
            return True

    return False


def count_proper_aims(
    x: tuple[int, int], y: tuple[int, int], simulation_size: int = 300
) -> int:
    counter = 0
    for i, j in product(
        range(0, simulation_size),
        range(-simulation_size, simulation_size),
    ):
        if simulate_aim(x, y, (i, j)):
            counter += 1

    return counter


# Tests

x, y = read_file(path.join(path.dirname(__file__), "./input-1.txt"))
result = count_proper_aims(x, y)
assert result == 112

# Result

x, y = read_file(path.join(path.dirname(__file__), "./input-2.txt"))
print(count_proper_aims(x, y))

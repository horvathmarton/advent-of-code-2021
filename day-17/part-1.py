from os import path
from re import findall


def read_file(name: str) -> str:
    with open(name) as f:
        params = findall(r"x=(-?\d*..-?\d*), y=(-?\d*..-?\d*)", f.read())

    x1, x2 = params[0][0].split("..")
    y1, y2 = params[0][1].split("..")

    return ((int(x1), int(x2)), (int(y1), int(y2)))


def simulate_vertical_movement(y: tuple[int, int], starting_speed: int) -> bool:
    position = 0
    speed = starting_speed
    max_position = 0

    while position >= min(y):
        position += speed
        speed -= 1

        max_position = max(position, max_position)

        if position in y:
            return True, max_position

    return False, max_position


def find_max_vertical_speed(y: tuple[int, int], simulation_size: int = 1_000) -> int:
    results = [simulate_vertical_movement(y, speed) for speed in range(simulation_size)]

    return next(results[i][1] for i in reversed(range(len(results))) if results[i][0])


# Tests

x, y = read_file(path.join(path.dirname(__file__), "./input-1.txt"))
assert find_max_vertical_speed(y) == 45

# Result

x, y = read_file(path.join(path.dirname(__file__), "./input-2.txt"))
print(find_max_vertical_speed(y))

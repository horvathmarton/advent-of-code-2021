def read_file(name: str) -> list[tuple[str, int]]:
    with open(name) as file:
        return [
            (line.split(" ")[0], int(line.split(" ")[1]))
            for line in file.read().split("\n")
        ]


def calculate_position(movements: list[tuple[str, int]]) -> tuple[int, int]:
    x = 0
    y = 0
    aim = 0

    for movement in movements:
        direction, value = movement

        if direction == "forward":
            x += value
            y += aim * value
        elif direction == "down":
            aim += value
        elif direction == "up":
            aim -= value
        else:
            raise Exception(f"Unknown direction {direction}")

    return x, y


input_1 = read_file("./input-1.txt")
input_2 = read_file("./input-2.txt")

x, y = calculate_position(input_1)
assert x == 15
assert y == 60
assert x * y == 900

x, y = calculate_position(input_2)
print(x * y)

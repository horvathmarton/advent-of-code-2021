def read_file(name: str) -> list[int]:
    with open(name) as file:
        return [int(num) for num in file.read().split("\n")]


def count_increases(measurements: list[int]) -> int:
    return len([i for i, j in zip(measurements, measurements[1:]) if i < j])


input_1 = read_file("./input-1.txt")
input_2 = read_file("./input-2.txt")

assert count_increases(input_1) == 7

print(count_increases(input_2))

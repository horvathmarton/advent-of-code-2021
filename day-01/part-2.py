def read_file(name: str) -> list[int]:
    with open(name) as file:
        return [int(num) for num in file.read().split("\n")]


def count_increases(measurements: list[int]) -> int:
    counter = 0
    for i in range(len(measurements) - 3):
        lst1 = measurements[i : i + 3]
        lst2 = measurements[i + 1 : i + 4]

        if sum(lst1) < sum(lst2):
            counter += 1

    return counter


input_1 = read_file("./input-1.txt")
input_2 = read_file("./input-2.txt")

assert count_increases(input_1) == 5

print(count_increases(input_2))

import numpy as np
from collections import Counter


def read_file(name: str) -> list[tuple[str, int]]:
    with open(name) as file:
        return np.array([list(binary) for binary in file.read().split("\n")])


def calculate_rates(binaries: np.array) -> tuple[int, int]:
    gamma = ""
    epsilon = ""

    for i in range(binaries.shape[1]):
        count = Counter(binaries[:, i])
        gamma += count.most_common()[0][0]
        epsilon += count.most_common()[1][0]

    return int(gamma, 2), int(epsilon, 2)


input_1 = read_file("./input-1.txt")
input_2 = read_file("./input-2.txt")

gamma, epsilon = calculate_rates(input_1)
assert gamma == 22
assert epsilon == 9
assert gamma * epsilon == 198

gamma, epsilon = calculate_rates(input_2)
print(gamma * epsilon)

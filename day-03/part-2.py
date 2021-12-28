import numpy as np
from collections import Counter


def read_file(name: str) -> list[tuple[str, int]]:
    with open(name) as file:
        return np.array([list(binary) for binary in file.read().split("\n")])


def calculate_rates(binaries: np.array) -> tuple[int, int]:
    oxigen_generator_rating = ""
    co2_scrubber_rating = ""
    filtered = binaries

    # Calculate oxigen rating.
    for i in range(binaries.shape[1]):
        count = Counter(filtered[:, i])
        most_commons = count.most_common()
        bit = (
            most_commons[0][0]
            if len(most_commons) == 1 or most_commons[0][1] != most_commons[1][1]
            else "1"
        )
        filtered = filtered[filtered[:, i] == bit]

        if len(filtered) == 1:
            oxigen_generator_rating = "".join(filtered[0])
            break
    else:
        raise Exception("Ambigous oxigen")

    filtered = binaries

    # Calculate CO2 rating.
    for i in range(binaries.shape[1]):
        count = Counter(filtered[:, i])
        most_commons = count.most_common()
        bit = (
            most_commons[1][0]
            if len(most_commons) == 1 or most_commons[0][1] != most_commons[1][1]
            else "0"
        )
        filtered = filtered[filtered[:, i] == bit]

        if len(filtered) == 1:
            co2_scrubber_rating = "".join(filtered[0])
            break
    else:
        raise Exception("Ambigous CO2")

    return int(oxigen_generator_rating, 2), int(co2_scrubber_rating, 2)


input_1 = read_file("./input-1.txt")
input_2 = read_file("./input-2.txt")

oxigen_generator_rating, co2_scrubber_rating = calculate_rates(input_1)
assert oxigen_generator_rating == 23
assert co2_scrubber_rating == 10
assert oxigen_generator_rating * co2_scrubber_rating == 230

oxigen_generator_rating, co2_scrubber_rating = calculate_rates(input_2)
print(oxigen_generator_rating * co2_scrubber_rating)

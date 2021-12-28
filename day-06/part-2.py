from os import path
from collections import Counter


def read_file(name: str) -> list[int]:
    with open(name) as f:
        return [int(num) for num in f.read().split(",")]


def simulate_day(counter: Counter) -> Counter:
    updated_counter = Counter()
    for key in counter:
        if not updated_counter[key]:
            updated_counter[key] = 0

        new_key = key - 1 if key > 0 else 6
        updated_counter[new_key] += counter[key]

    if counter[0]:
        updated_counter[8] = counter[0]

    return updated_counter


def simulate(fish: list[int], days: int) -> int:
    result = Counter(fish)
    for i in range(days):
        result = simulate_day(result)

    return sum(result.values())


lines = read_file(path.join(path.dirname(__file__), "./input-1.txt"))

fish_count = simulate(lines, 18)
assert fish_count == 26
fish_count = simulate(lines, 80)
assert fish_count == 5934
fish_count = simulate(lines, 256)
assert fish_count == 26984457539

lines = read_file(path.join(path.dirname(__file__), "./input-2.txt"))

fish_count = simulate(lines, 256)
print(fish_count)

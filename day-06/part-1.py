from os import path


def read_file(name: str) -> list[int]:
    with open(name) as f:
        return [int(num) for num in f.read().split(",")]


def simulate_day(fish: list[int]) -> list[int]:
    result = []
    new_fish = []
    for f in fish:
        if f == 0:
            new_fish.append(8)
        result.append(f - 1 if f > 0 else 6)

    result += new_fish

    return result


def simulate(fish: list[int], days: int) -> int:
    result = fish
    for i in range(days):
        result = simulate_day(result)

    return len(result)


lines = read_file(path.join(path.dirname(__file__), "./input-1.txt"))

fish_count = simulate(lines, 18)
assert fish_count == 26
fish_count = simulate(lines, 80)
assert fish_count == 5934

lines = read_file(path.join(path.dirname(__file__), "./input-2.txt"))

fish_count = simulate(lines, 80)
print(fish_count)

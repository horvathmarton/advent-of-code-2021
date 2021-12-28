from os import path
from functools import cache


def read_file(name: str) -> list[int]:
    with open(name) as f:
        return [int(num) for num in f.read().split(",")]


@cache
def fuel_cost(length: int) -> int:
    return sum(range(length + 1))


def simulate(positions: list[int]) -> int:
    max_position = max(positions)

    costs = {}
    for i in range(max_position):
        fuel_costs = [fuel_cost(abs(position - i)) for position in positions]
        costs[i] = sum(fuel_costs)

    return min(costs.values())


positions = read_file(path.join(path.dirname(__file__), "./input-1.txt"))

cost = fuel_cost(1)
assert cost == 1
cost = fuel_cost(2)
assert cost == 3
cost = fuel_cost(11)
assert cost == 66

cost = simulate(positions)
assert cost == 168

positions = read_file(path.join(path.dirname(__file__), "./input-2.txt"))

cost = simulate(positions)
print(cost)

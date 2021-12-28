from os import path


def read_file(name: str) -> list[int]:
    with open(name) as f:
        return [int(num) for num in f.read().split(",")]


def simulate(positions: list[int]) -> int:
    max_position = max(positions)

    costs = {}
    for i in range(max_position):
        fuel_costs = [abs(position - i) for position in positions]
        costs[i] = sum(fuel_costs)

    return min(costs.values())


positions = read_file(path.join(path.dirname(__file__), "./input-1.txt"))

fuel_cost = simulate(positions)
assert fuel_cost == 37

positions = read_file(path.join(path.dirname(__file__), "./input-2.txt"))

fuel_cost = simulate(positions)
print(fuel_cost)

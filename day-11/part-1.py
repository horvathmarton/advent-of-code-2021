from os import path


class Octopus:
    flashed = False

    @property
    def ready_to_flash(self) -> bool:
        return self.energy > 9

    def __init__(self, energy):
        self.energy = energy

    def charge(self) -> None:
        if not self.flashed:
            self.energy += 1

    def flash(self) -> None:
        self.energy = 0
        self.flashed = True

    def reset(self) -> None:
        self.flashed = False


OctopusGrid = list[list[Octopus]]


def read_file(name: str) -> OctopusGrid:
    with open(name) as f:
        return [
            [Octopus(int(energy)) for energy in list(line)]
            for line in f.read().split("\n")
        ]


def get_neighbors(octopuses: OctopusGrid, x: int, y: int):
    neighbors = {}

    if y > 0:
        neighbors["top"] = octopuses[y - 1][x]

    if y < len(octopuses) - 1:
        neighbors["bottom"] = octopuses[y + 1][x]

    if x > 0:
        neighbors["left"] = octopuses[y][x - 1]

    if x < len(octopuses[0]) - 1:
        neighbors["right"] = octopuses[y][x + 1]

    if y > 0 and x > 0:
        neighbors["top-left"] = octopuses[y - 1][x - 1]

    if y > 0 and x < len(octopuses[0]) - 1:
        neighbors["top-right"] = octopuses[y - 1][x + 1]

    if y < len(octopuses) - 1 and x > 0:
        neighbors["bottom-left"] = octopuses[y + 1][x - 1]

    if y < len(octopuses) - 1 and x < len(octopuses[0]) - 1:
        neighbors["bottom-right"] = octopuses[y + 1][x + 1]

    return neighbors


def simulate_tick(octopuses: OctopusGrid) -> tuple[OctopusGrid, int]:
    for line in octopuses:
        for octopus in line:
            octopus.reset()
            # Rule 1
            octopus.charge()

    flashes = 0
    flash_happened = True
    while flash_happened:
        flash_happened = False

        for y, line in enumerate(octopuses):
            for x, octopus in enumerate(line):
                if octopus.ready_to_flash:
                    neighs = get_neighbors(octopuses, x, y)
                    # Rule 2
                    for neighbor in neighs.values():
                        neighbor.charge()
                    # Rule 3
                    octopus.flash()
                    flash_happened = True
                    flashes += 1

    return octopuses, flashes


def count_flashes(octopuses: OctopusGrid, ticks: int) -> int:
    grid = octopuses
    flash_count = 0

    for i in range(ticks):
        grid, flashes = simulate_tick(grid)
        flash_count += flashes
        # print(f"Tick {i + 1}: {flash_count} flashes.")

    return flash_count


octopuses = read_file(path.join(path.dirname(__file__), "./input-1.txt"))
flashes = count_flashes(octopuses, ticks=10)
assert flashes == 204
octopuses = read_file(path.join(path.dirname(__file__), "./input-1.txt"))
flashes = count_flashes(octopuses, ticks=100)
assert flashes == 1656

octopuses = read_file(path.join(path.dirname(__file__), "./input-2.txt"))
flashes = count_flashes(octopuses, ticks=100)
print(flashes)

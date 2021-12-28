from os import path


def read_file(name: str) -> str:
    with open(name) as f:
        lines = f.read().splitlines()

    one = lines[0].split()[-1]
    two = lines[1].split()[-1]

    return int(one), int(two)


def dice() -> int:
    while True:
        for i in range(1, 101):
            yield i


def wrap_position(curr: int, step: int) -> int:
    return (curr - 1 + step) % 10 + 1


def simulate_game(one: int, two: int) -> tuple[int, int]:
    dice_rolls = 0
    current_player = 0
    players = [
        {"name": "p1", "position": one, "score": 0},
        {"name": "p2", "position": two, "score": 0},
    ]
    d = dice()

    while players[not current_player]["score"] < 1_000:
        player = players[current_player]
        step = sum(next(d) for _ in range(3))
        dice_rolls += 3

        player["position"] = wrap_position(player["position"], step)
        player["score"] += player["position"]

        current_player = not current_player

    return players[current_player]["score"], dice_rolls


one, two = read_file(path.join(path.dirname(__file__), "./input-1.txt"))
result = simulate_game(one, two)
assert result[0] == 745
assert result[1] == 993

one, two = read_file(path.join(path.dirname(__file__), "./input-2.txt"))
result = simulate_game(one, two)
print(result[0] * result[1])

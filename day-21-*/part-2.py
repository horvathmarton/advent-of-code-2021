from functools import cache

MINIMUM_ENDING_SCORE = 21

with open("./input-2.txt") as f:
    positions = [int(v.split(": ")[1]) - 1 for v in f.read().splitlines()]
player_count = len(positions)
scores = [0 for _ in range(player_count)]


def get_wins(turn, positions, scores):
    results = [
        roll_dice(turn, n + 1, tuple(positions), tuple(scores)) for n in range(3)
    ]
    return list(map(sum, zip(*results)))


@cache
def roll_dice(turn, roll, positions, scores):
    turn += 1
    player_index = ((turn - 1) // 3) % player_count
    positions, scores = list(positions), list(scores)
    positions[player_index] = (positions[player_index] + roll) % 10
    if (turn % 3) == 0:
        scores[player_index] += positions[player_index] + 1
    if all(s < MINIMUM_ENDING_SCORE for s in scores):
        return get_wins(turn, positions, scores)
    else:
        return [(i == player_index) for i in range(len(positions))]


print(max(get_wins(0, positions, scores)))

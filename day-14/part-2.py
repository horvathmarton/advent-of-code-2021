from os import path
from collections import Counter


def read_file(name: str) -> tuple[str, dict[str, str]]:
    with open(name) as f:
        letters, lines = f.read().split("\n\n")

    instructions = {}
    for instruction in lines.split("\n"):
        to, letter = instruction.split(" -> ")
        instructions[to] = letter

    return letters, instructions


def simulate_round(
    counter: Counter, instructions: dict[str, str], insert_counter: Counter
) -> Counter:
    new_counter = Counter(counter)

    for place, letter in instructions.items():
        if counter[place]:
            first_new_seq = place[0] + letter
            second_new_seq = letter + place[1]

            new_counter[first_new_seq] += counter[place]
            new_counter[second_new_seq] += counter[place]
            new_counter[place] -= counter[place]

            insert_counter[letter] += counter[place]

    return new_counter


def create_polymer(
    chain: str, instructions: list[dict[str, str]], steps: int
) -> Counter:
    insert_counter = Counter(chain)
    counter = Counter((first + second for first, second in zip(chain, chain[1:])))

    for i in range(steps):
        counter = simulate_round(counter, instructions, insert_counter)

    return insert_counter


chain, instructions = read_file(path.join(path.dirname(__file__), "./input-1.txt"))
counter = create_polymer(chain, instructions, 40)

most_common = counter.most_common()[0][1]
least_common = counter.most_common()[-1][1]

assert most_common - least_common == 2188189693529

head, instructions = read_file(path.join(path.dirname(__file__), "./input-2.txt"))
counter = create_polymer(head, instructions, 40)

most_common = counter.most_common()[0][1]
least_common = counter.most_common()[-1][1]

print(most_common - least_common)

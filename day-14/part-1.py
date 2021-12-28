from os import path
from collections import Counter


class Node:
    def __init__(self, letter: str, next_node: "Node" = None):
        self.letter = letter
        self.next = next_node
        self.inserted = None

    def __repr__(self) -> str:
        chain = self.letter
        n = self.inserted or self.next
        while n:
            chain += n.letter
            n = n.inserted or n.next

        return chain


def read_file(name: str) -> tuple[Node, dict[str, str]]:
    with open(name) as f:
        letters, lines = f.read().split("\n\n")

    prev = None
    for letter in letters:
        node = Node(letter)

        if prev:
            prev.next = node
        else:
            head = node

        prev = node

    instructions = {}
    for instruction in lines.split("\n"):
        to, letter = instruction.split(" -> ")
        instructions[to] = letter

    return head, instructions


def simulate_round(head: Node, instructions: dict[str, str]) -> Node:
    node = head
    while node.next or node.inserted:
        if node.inserted:
            node.next = node.inserted

        pair = node.letter + node.next.letter
        if pair in instructions:
            node.inserted = Node(instructions[pair], node.next)

        node = node.next

    return head


def create_polymer(head: Node, instructions: list[dict[str, str]], steps: int):
    for _ in range(steps):
        head = simulate_round(head, instructions)

    return head


head, instructions = read_file(path.join(path.dirname(__file__), "./input-1.txt"))
polymer = create_polymer(head, instructions, 10)
counter = Counter(str(polymer))

most_common = counter.most_common()[0][1]
least_common = counter.most_common()[-1][1]

assert most_common - least_common == 1588

head, instructions = read_file(path.join(path.dirname(__file__), "./input-2.txt"))
polymer = create_polymer(head, instructions, 10)
counter = Counter(str(polymer))

most_common = counter.most_common()[0][1]
least_common = counter.most_common()[-1][1]

print(most_common - least_common)

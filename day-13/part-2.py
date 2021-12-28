from os import path
from itertools import zip_longest


class Paper:
    def __init__(self, x: int, y: int):
        self.content = [[False for _ in range(x)] for _ in range(y)]

    def __str__(self):
        return "\n".join(
            (
                "".join(("#" if letter else "." for letter in line))
                for line in self.content
            )
        )

    def mark(self, x: int, y: int) -> None:
        self.content[y][x] = True

    def fold_vertically(self, x: int) -> None:
        new_lines = []
        for line in self.content:
            base = line[:x]
            fold = line[x + 1 :][::-1]

            new_lines.append(
                [(b or f) for b, f in zip_longest(base, fold, fillvalue=False)]
            )

        self.content = new_lines

    def fold_horizontally(self, y: int) -> None:
        base = self.content[:y]
        fold = self.content[y + 1 :][::-1]

        new_lines = []
        for b, f in zip_longest(base, fold, fillvalue=[]):
            new_lines.append([a or b for a, b in zip_longest(b, f, fillvalue=False)])

        self.content = new_lines

    def count_marks(self) -> int:
        return sum((sum(line) for line in self.content))


def read_file(name: str) -> Paper:
    with open(name) as f:
        letters, instructions = f.read().split("\n\n")

    marks = []
    for letter in letters.split("\n"):
        x, y = letter.split(",")
        marks.append((int(x), int(y)))

    max_x = max((x for x, y in marks)) + 1
    max_y = max((y for x, y in marks)) + 1
    paper = Paper(max_x, max_y)

    for x, y in marks:
        paper.mark(x, y)

    return paper, instructions.split("\n")


def fold_paper(paper: Paper, instructions: list[str]):
    for instruction in instructions:
        direction, line = instruction.split()[-1].split("=")
        if direction == "y":
            paper.fold_horizontally(int(line))
        else:
            paper.fold_vertically(int(line))

        print(paper, end="\n\n\n")


paper, instructions = read_file(path.join(path.dirname(__file__), "./input-1.txt"))
paper = fold_paper(paper, instructions)

paper, instructions = read_file(path.join(path.dirname(__file__), "./input-2.txt"))
paper = fold_paper(paper, instructions)

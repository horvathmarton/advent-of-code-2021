import numpy as np
from os import path


def read_file(name: str) -> tuple[list[int], list[np.array]]:
    tables = []

    with open(name) as file:
        numbers = [int(num) for num in file.readline().split(",")]
        raw_tables = file.read().split("\n\n")

        for table in raw_tables:
            t = []

            for line in table.split("\n"):
                if not line:
                    continue

                t.append([int(cell) for cell in line.split(" ") if cell])

            tables.append(np.array([t, np.zeros((5, 5), dtype=bool)]))

    return numbers, tables


def is_winner(table: np.array):
    for i in range(table.shape[1]):
        row_marks = np.count_nonzero(table[1, i, :])
        if row_marks == 5:
            return True

        col_marks = np.count_nonzero(table[1, :, i])
        if col_marks == 5:
            return True

    return False


def play_bingo(numbers: list[int], tables: list[np.array]) -> tuple[int, int]:
    for number in numbers:
        for table in tables:
            table[1, table[0, :, :] == number] = True

            if is_winner(table):
                return table[0, table[1, :, :] == False].sum(), number
    else:
        print("No winner")


numbers, tables = read_file(path.join(path.dirname(__file__), "./input-1.txt"))

winner_sum, last_call = play_bingo(numbers, tables)
assert winner_sum == 188
assert last_call == 24
assert winner_sum * last_call == 4512

numbers, tables = read_file(path.join(path.dirname(__file__), "./input-2.txt"))

winner_sum, last_call = play_bingo(numbers, tables)
print(winner_sum * last_call)

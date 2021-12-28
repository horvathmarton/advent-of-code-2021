from os import path
from collections import Counter


def read_file(name: str) -> list[int]:
    with open(name) as f:
        lines = []
        for line in f.read().split("\n"):
            reference_digits, input_digits = line.split("|")
            reference_digits = [word for word in reference_digits.split() if word]
            input_digits = [word for word in input_digits.split() if word]

            lines.append((reference_digits, input_digits))

        return lines


def reverse_engineer_digits(digits: tuple[list[str], list[str]]) -> Counter:
    counter = Counter()

    for line in digits:
        _, input_digits = line

        counter += Counter([len(word) for word in input_digits])

    return Counter(
        {
            "0,6,9": counter[6],
            "1": counter[2],
            "2,3,5": counter[5],
            "4": counter[4],
            "7": counter[3],
            "8": counter[7],
        }
    )


digits = read_file(path.join(path.dirname(__file__), "./input-1.txt"))

digit_count = reverse_engineer_digits(digits)
assert digit_count["1"] + digit_count["4"] + digit_count["7"] + digit_count["8"] == 26

digits = read_file(path.join(path.dirname(__file__), "./input-2.txt"))

digit_count = reverse_engineer_digits(digits)
print(digit_count["1"] + digit_count["4"] + digit_count["7"] + digit_count["8"])

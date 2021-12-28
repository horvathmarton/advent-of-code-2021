from os import path
from collections import Counter


ALPHABET = "abcdefg"


def read_file(name: str) -> list[int]:
    with open(name) as f:
        lines = []
        for line in f.read().split("\n"):
            reference_digits, input_digits = line.split("|")
            reference_digits = [word for word in reference_digits.split() if word]
            input_digits = [word for word in input_digits.split() if word]

            lines.append((reference_digits, input_digits))

        return lines


def normalize_str(s: str) -> str:
    return "".join(sorted(list(s)))


def reverse_engineer_mappings(
    reference_digits: list[str], input_digits: list[str]
) -> tuple[dict[str, str], dict[str, str]]:
    counter = Counter(len(item) for item in reference_digits)

    if counter[6] == 0 or counter[2] == 0 or counter[4] == 0 or counter[3] == 0:
        raise Error("Missing reference numbers")

    number_mapping = {
        "1": next(item for item in reference_digits if len(item) == 2),
        "4": next(item for item in reference_digits if len(item) == 4),
        "7": next(item for item in reference_digits if len(item) == 3),
        "8": next(item for item in reference_digits if len(item) == 7),
    }

    one_segment_1, one_segment_2 = list(number_mapping["1"])

    # Three is the only 5 segment number that contains both segment from one.
    number_mapping["3"] = next(
        item
        for item in reference_digits
        if len(item) == 5 and one_segment_1 in item and one_segment_2 in item
    )
    # Six is a 6 segment number that doesn't contain both segment from one.
    number_mapping["6"] = next(
        item
        for item in reference_digits
        if len(item) == 6 and (one_segment_1 not in item or one_segment_2 not in item)
    )

    segment_mapping = {
        "a": next(
            letter
            for letter in ALPHABET
            if letter in number_mapping["7"] and letter not in number_mapping["1"]
        ),
        "c": next(letter for letter in ALPHABET if letter not in number_mapping["6"]),
    }

    segment_mapping["b"] = next(
        letter
        for letter in ALPHABET
        if letter in number_mapping["4"] and letter not in number_mapping["3"]
    )

    # The d the segment present in four not in one (this is two segments so far).
    # From the two candidates we need the one that is not the c segment.
    segment_mapping["d"] = next(
        letter
        for letter in ALPHABET
        if letter not in number_mapping["1"]
        and letter in number_mapping["4"]
        and letter != segment_mapping["b"]
    )

    number_mapping["0"] = next(
        item
        for item in reference_digits
        if len(item) == 6 and segment_mapping["d"] not in item
    )
    number_mapping["9"] = next(
        item
        for item in reference_digits
        if len(item) == 6
        and item != number_mapping["0"]
        and item != number_mapping["6"]
    )

    number_mapping["2"] = next(
        item
        for item in reference_digits
        if len(item) == 5
        and item != number_mapping["3"]
        and segment_mapping["c"] in item
    )
    number_mapping["5"] = next(
        item
        for item in reference_digits
        if len(item) == 5
        and item != number_mapping["3"]
        and segment_mapping["b"] in item
    )

    return number_mapping, segment_mapping


def reverse_engineer_digits(
    reference_digits: list[str], input_digits: list[str]
) -> int:
    number_mapping, _ = reverse_engineer_mappings(reference_digits, input_digits)
    inverted_number_mapping = {normalize_str(v): k for k, v in number_mapping.items()}

    return int(
        "".join([inverted_number_mapping[normalize_str(word)] for word in input_digits])
    )


digits = read_file(path.join(path.dirname(__file__), "./input-1.txt"))

s = sum([reverse_engineer_digits(*d) for d in digits])
assert s == 61229

digits = read_file(path.join(path.dirname(__file__), "./input-2.txt"))

s = sum([reverse_engineer_digits(*d) for d in digits])
print(s)

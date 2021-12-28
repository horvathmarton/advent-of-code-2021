from os import path


def read_file(name: str) -> list[int]:
    with open(name) as f:
        return f.read().split("\n")


completion_weight = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}
matching_paren = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def check_syntax(code: str) -> tuple[int, int]:
    if len(code) < 1:
        raise Exception("Something is not right.")

    current_char = code[0]
    checked_chars = 1
    completion_score = 0

    if current_char in ")}]>":
        raise Exception("Corrupted line.")

    if len(code) < 2:
        missing = completion_weight[matching_paren[current_char]]
        return checked_chars, missing

    while code[checked_chars : checked_chars + 1] != matching_paren[current_char]:
        if not len(code[checked_chars:]):
            missing = completion_weight[matching_paren[current_char]]
            return checked_chars, missing

        checked, missing = check_syntax(code[checked_chars:])
        checked_chars += checked

        if missing:
            completion_score = (
                5 * missing + completion_weight[matching_paren[current_char]]
            )
            return checked_chars, completion_score
    else:
        checked_chars += 1
        return checked_chars, 0


def calculation_completion_score(codes: list[str]) -> int:
    completion_scores = []
    for code in codes:
        try:
            _, score = check_syntax(code)
            if score:
                completion_scores.append(score)
        except Exception as e:
            if str(e) == "Corrupted line.":
                pass
            else:
                raise

    return sorted(completion_scores)[len(completion_scores) // 2]


codes = read_file(path.join(path.dirname(__file__), "./input-1.txt"))
score = calculation_completion_score(codes)
assert score == 288957

codes = read_file(path.join(path.dirname(__file__), "./input-2.txt"))
score = calculation_completion_score(codes)
print(score)

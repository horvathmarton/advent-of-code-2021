from os import path


def read_file(name: str) -> list[int]:
    with open(name) as f:
        return f.read().split("\n")


error_weight = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
matching_paren = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def check_syntax(code: str) -> int:
    if len(code) < 2:
        raise Exception("Incomplete line")

    current_char = code[0]
    checked_chars = 1

    if current_char in ")}]>":
        raise Exception(error_weight[current_char])

    while code[checked_chars : checked_chars + 1] != matching_paren[current_char]:
        checked_chars += check_syntax(code[checked_chars:])
    else:
        checked_chars += 1
        return checked_chars


codes = read_file(path.join(path.dirname(__file__), "./input-1.txt"))

error_score = 0
for code in codes:
    try:
        checked_length = check_syntax(code)
        # assert checked_length == len(code)
    except Exception as e:
        if str(e) == "Incomplete line":
            pass
        else:
            error_score += e.args[0]

assert error_score == 26397

codes = read_file(path.join(path.dirname(__file__), "./input-2.txt"))

error_score = 0
for code in codes:
    try:
        checked_length = check_syntax(code)
        # assert checked_length == len(code)
    except Exception as e:
        if str(e) == "Incomplete line":
            pass
        else:
            error_score += e.args[0]

print(error_score)

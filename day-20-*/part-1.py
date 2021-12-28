import numpy as np
from time import perf_counter


def scanner_enhance(file_path, max_run):

    with open(file_path) as fin:
        algo, image = fin.read().strip().split("\n\n")

    algo_b = {}

    for i, val in enumerate(algo):
        if val == "#":
            algo_b[i] = 1
        else:
            algo_b[i] = 0

    image = image.split("\n")
    image_b = np.zeros((len(image), len(image[0])), dtype=int)

    for i, row in enumerate(image):
        for j, val in enumerate(row):
            if val == "#":
                image_b[i, j] = 1
            else:
                image_b[i, j] = 0

    run = 1

    while run <= max_run:
        if algo_b[1] == 1 and not run % 2:
            image_pad = np.ones((image_b.shape[0] + 4, image_b.shape[1] + 4), dtype=int)
        else:
            image_pad = np.zeros(
                (image_b.shape[0] + 4, image_b.shape[1] + 4), dtype=int
            )

        image_pad[2:-2, 2:-2] = image_b

        e_image = np.zeros((image_b.shape[0] + 2, image_b.shape[1] + 2), dtype=int)

        for loc, val in np.ndenumerate(image_pad):
            x, y = loc
            if x in range(1, len(image_pad) - 1) and y in range(1, len(image_pad) - 1):
                sub_pix = image_pad[x - 1 : x + 2, y - 1 : y + 2]
                pix_str = ""
                for row in sub_pix:
                    for s_val in row:
                        pix_str += str(s_val)

                e_image[x - 1, y - 1] = algo_b[int(pix_str, 2)]

        image_b = e_image.copy()
        run += 1

    return np.count_nonzero(image_b)


def main():

    # assert scanner_enhance("./input-1.txt", 2) == 35
    # print(scanner_enhance("./input-2.txt", 2))

    # assert scanner_enhance("./input-1.txt", 50) == 3351
    start = perf_counter()
    # print(scanner_enhance("./input-2.txt", 50), perf_counter() - start)


if __name__ == "__main__":
    main()
from itertools import product
from typing import Generator


def parse_input(filepath):
    with open(filepath, "r") as f:
        algorithm, image = f.read().split("\n\n")
        image_map = {}
        for y, row in enumerate(image.split("\n")):
            for x, col in enumerate(row):
                image_map[complex(x, y)] = col
    return algorithm, image_map


def binary_to_dec(bin_number):
    return int(bin_number, 2)


def str_to_bin(arr: list[str]) -> list[str]:
    return ["0" if i == "." else "1" for i in arr]


def get_edges(image_map: dict[complex, str]) -> tuple[int, ...]:
    x_min, y_min, x_max, y_max = (
        float("inf"),
        float("inf"),
        float("-inf"),
        float("-inf"),
    )
    for position in image_map:
        x = position.real
        y = position.imag
        if x < x_min:
            x_min = x
        if y < y_min:
            y_min = y
        if x > x_max:
            x_max = x
        if y > y_max:
            y_max = y
    return tuple(map(int, (x_min, y_min, x_max, y_max)))


def get_adjacent(
    coordinate: complex,
    window=(
        complex(-1, -1),
        complex(0, -1),
        complex(1, -1),
        complex(-1, 0),
        complex(0, 0),
        complex(1, 0),
        complex(-1, 1),
        complex(0, 1),
        complex(1, 1),
    ),
) -> Generator[complex, None, None]:
    for adjacent in window:
        yield coordinate + adjacent


def process_image(image, algorithm, nth_iteration=None):
    edges = get_edges(image)
    if nth_iteration:
        default = "#" if nth_iteration % 2 != 0 else "."
    else:
        default = "."
    new_map = {}
    for x, y in product(
        range(edges[0] - 1, edges[2] + 2), range(edges[1] - 1, edges[3] + 2)
    ):
        next_num = [image.get(coord, default) for coord in get_adjacent(complex(x, y))]
        next_num_bin = "".join(str_to_bin(next_num))
        algo_idx_int = binary_to_dec(next_num_bin)
        new_map[complex(x, y)] = algorithm[algo_idx_int]
    return new_map


def sum_image(img) -> int:
    n = 0
    for val in img.values():
        if val == "#":
            n += 1
    return n


def part_a():
    fp = r"./input-2.txt"
    algo, img = parse_input(fp)

    for i in range(2):
        img = process_image(img, algo, i)
    return sum_image(img)


def part_b():
    fp = r"./input-2.txt"
    algo, img = parse_input(fp)

    for i in range(50):
        img = process_image(img, algo, i)
    return sum_image(img)


if __name__ == "__main__":
    print(part_a())
    print(part_b())

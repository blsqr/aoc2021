"""Solution for Day 01: Sonar Sweep"""

from ..tools import relative_to_file

DATA_FILE = relative_to_file(__file__, "input.txt")


def solve_part1(data_file: str = DATA_FILE) -> int:
    with open(DATA_FILE, mode="r") as f:
        data = [int(v) for v in f.readlines()]

    diff_was_positive = [v2 > v1 for v1, v2 in zip(data[:-1], data[1:])]
    return sum(diff_was_positive)

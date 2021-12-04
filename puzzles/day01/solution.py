"""Solution for Day 01: Sonar Sweep

For puzzle text, see: https://adventofcode.com/2021/day/1
"""

from ..tools import relative_to_file

DATA_FILE = relative_to_file(__file__, "input.txt")


def load_data(fpath: str) -> list:
    """Loads the input data as list of integers"""
    with open(fpath, mode="r") as f:
        data = [int(v) for v in f.readlines()]
    return data


def solve_part1(data_file: str = DATA_FILE) -> int:
    """Computes the solution for part 1"""
    data = load_data(data_file)
    diff_was_positive = [v2 > v1 for v1, v2 in zip(data[:-1], data[1:])]
    return sum(diff_was_positive)


def solve_part2(data_file: str = DATA_FILE) -> int:
    """Computes the solution for part 2"""
    data = load_data(data_file)

    # Want sliding window of sums of width 3
    sliding_window = [
        v1 + v2 + v3 for v1, v2, v3 in zip(data[:-2], data[1:-1], data[2:])
    ]
    # NOTE "Stop when there aren't enough measurements left to create a new
    #       three-measurement sum."
    #      This zip approach fulfills that requirement.

    window_diff_was_positive = [
        s2 > s1 for s1, s2 in zip(sliding_window[:-1], sliding_window[1:])
    ]
    return sum(window_diff_was_positive)

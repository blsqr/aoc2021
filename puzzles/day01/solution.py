"""Solution for Day 01: Sonar Sweep

For puzzle text, see: https://adventofcode.com/2021/day/1
"""

from ..tools import relative_to_file, load_input

DAY = 1
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT = """
    199
    200
    208
    210
    200
    207
    240
    269
    260
    263
"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)


# -- Part 1 -------------------------------------------------------------------

def solve_part1(*, input_mode: str) -> int:
    """Computes the solution for part 1"""
    data = load_input(input_mode, **INPUT_KWARGS)
    data = [int(v) for v in data]

    diff_was_positive = [v2 > v1 for v1, v2 in zip(data[:-1], data[1:])]
    return sum(diff_was_positive)


# -- Part 2 -------------------------------------------------------------------

def solve_part2(*, input_mode: str) -> int:
    """Computes the solution for part 2"""
    data = load_input(input_mode, **INPUT_KWARGS)
    data = [int(v) for v in data]

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

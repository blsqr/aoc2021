"""Solution for Day 5: Hydrothermal Venture

For puzzle text, see: https://adventofcode.com/2021/day/5
"""
from typing import List, Tuple

import numpy as np

from ..tools import relative_to_file, load_input

DAY = 5
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)


def parse_coords(line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Parses the coordinates of a single line from the input string"""
    pt1, pt2 = line.split(" -> ")
    pt1 = [int(v) for v in pt1.split(",")]
    pt2 = [int(v) for v in pt2.split(",")]
    return tuple(pt1), tuple(pt2)

def find_coords_maxval(lines) -> Tuple[int, int]:
    """Finds the largest values in x and y coordinates"""
    x_max, y_max = 0, 0
    for (x1, y1), (x2, y2) in lines:
        x_max = max(x_max, x1, x2)
        y_max = max(y_max, y1, y2)

    return x_max, y_max

def mark_line(pt1, pt2, *, domain: np.ndarray) -> None:
    """In-place marks a line pt1 -> pt2 in the domain"""
    x1, y1 = pt1
    x2, y2 = pt2
    print(f"Line  ({x1:3d}, {y1:3d})  ->  ({x2:3d}, {y2:3d})  ... ", end="")

    # Compute the required increment, which is used in the specification of the
    # range function used in setting domain values
    get_step = lambda c1, c2: +1 if c1 <= c2 else -1

    # Distinguish horizontal and vertical lines
    if x1 == x2:
        y_step = get_step(y1, y2)
        domain[x1, range(y1, y2 + y_step, y_step)] += 1
        print("marked vertical line.")

    elif y1 == y2:
        x_step = get_step(x1, x2)
        domain[range(x1, x2 + x_step, x_step), y1] += 1
        print("marked horizontal line.")

    elif abs(x2 - x1) == abs(y2 - y1):
        x_step = get_step(x1, x2)
        y_step = get_step(y1, y2)

        for x, y in zip(
            range(x1, x2 + x_step, x_step),
            range(y1, y2 + y_step, y_step),
        ):
            domain[x, y] += 1
        print("marked diagonal line.")

    else:
        raise NotImplementedError(
            "Cannot handle lines that are not horizontal, vertical, or "
            "exactly diagonal!"
        )


# -- Part 1 -------------------------------------------------------------------

def solve_part1(*, input_mode: str) -> int:
    """Computes the solution for part 1"""
    data = load_input(input_mode, **INPUT_KWARGS)
    lines = [parse_coords(line) for line in data]

    # Construct domain
    x_max, y_max = find_coords_maxval(lines)
    domain = np.zeros((x_max+1, y_max+1), dtype=int)
    print(
        f"Have {len(lines)} lines of hydrothermal vents "
        f"in a domain of shape {domain.shape}."
    )

    for line in lines:
        mark_line(*line, domain=domain)

    print(f"\nFinal domain map:\n{domain.T}")

    # Count points where at least two lines overlap
    return np.sum(domain >= 2)


# -- Part 2 -------------------------------------------------------------------

def solve_part2(*, input_mode: str) -> int:
    """Computes the solution for part 2"""
    return solve_part1(input_mode=input_mode)
    

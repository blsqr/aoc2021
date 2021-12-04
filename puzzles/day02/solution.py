"""Solution for Day 2: Dive!

For puzzle text, see: https://adventofcode.com/2021/day/2
"""

from typing import Tuple, Callable

from ..tools import relative_to_file

DATA_FILE = relative_to_file(__file__, "input.txt")

DIRECTION_OPERATORS = dict(
    forward = lambda h, d, delta_h: (h + delta_h, d),
    down =    lambda h, d, delta_d: (h, d + delta_d),
    up =      lambda h, d, delta_d: (h, d - delta_d),
)


def load_data(fpath: str):
    """Loads the input data into a """
    with open(fpath, mode="r") as f:
        data = f.readlines()
    return data


def parse_line(line: str) -> Tuple[Callable, int]:
    """Parses a line of the input data into (operator, distance) form"""
    direction, distance = line.strip().split(" ")
    return DIRECTION_OPERATORS[direction], int(distance)


def solve_part1(data_file: str = DATA_FILE):
    """Computes the solution for part 1"""
    data = load_data(data_file)

    # Parse the instructions into (operator, delta) pairs
    instructions = [parse_line(line) for line in data]

    # Now apply the instructions, starting from (horizontal 0, depth 0)
    pos = (0, 0)
    for op, delta in instructions:
        pos = op(*pos, delta)
        # print(pos)
    print(f"Final position:  {pos}")

    # The solution is these values multiplied
    return pos[0] * pos[1]


def solve_part2(data_file: str = DATA_FILE) -> int:
    """Computes the solution for part 2"""
    raise NotImplementedError()
    

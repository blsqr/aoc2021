"""Solution for Day 2: Dive!

For puzzle text, see: https://adventofcode.com/2021/day/2
"""

from typing import Tuple, Callable

from ..tools import relative_to_file, load_input

DAY = 2
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT = """
    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2
"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)


# -- Part 1 -------------------------------------------------------------------

def parse_line_simple(line: str) -> Tuple[Callable, int]:
    """Parses a line of the input data into (operator, args) form"""
    DIRECTION_OPERATORS = dict(
        forward = lambda x, y, delta_x: (x + delta_x, y),
        down =    lambda x, y, delta_y: (x, y + delta_y),
        up =      lambda x, y, delta_y: (x, y - delta_y),
    )

    direction, arg = line.strip().split(" ")
    return DIRECTION_OPERATORS[direction], int(arg)


def solve_part1(*, input_mode: str) -> int:
    """Computes the solution for part 1"""
    data = load_input(input_mode, **INPUT_KWARGS)

    # Parse the instructions into (operator, delta) pairs
    instructions = [parse_line_simple(line) for line in data]

    # Now apply the instructions, starting from (horizontal 0, depth 0)
    pos = (0, 0)
    for op, delta in instructions:
        pos = op(*pos, delta)
        # print(pos)
    print(f"Final position:  {pos}")

    # The solution is these values multiplied
    return pos[0] * pos[1]


# -- Part 2 -------------------------------------------------------------------

def parse_line_with_aim(line: str) -> Tuple[Callable, int]:
    """Parses a line of the input data into (operator, args) form"""
    DIRECTION_OPERATORS = dict(
        forward = lambda x, y, a, delta: (x + delta, y + a * delta, a),
        down =    lambda x, y, a, delta: (x, y, a + delta),
        up =      lambda x, y, a, delta: (x, y, a - delta),
    )

    direction, distance = line.strip().split(" ")
    return DIRECTION_OPERATORS[direction], int(distance)


def solve_part2(*, input_mode: str) -> int:
    """Computes the solution for part 2"""
    data = load_input(input_mode, **INPUT_KWARGS)

    # Parse the instructions into (operator, delta) pairs
    instructions = [parse_line_with_aim(line) for line in data]

    # Now apply the instructions, starting from (horizontal 0, depth 0, aim 0)
    state = (0, 0, 0)
    for op, delta in instructions:
        state = op(*state, delta)

    print(f"Final state (x, y, aim):  {state}")

    # The solution is these values multiplied
    return state[0] * state[1]

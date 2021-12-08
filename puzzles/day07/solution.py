"""Solution for Day 7: The Treachery of Whales

For puzzle text, see: https://adventofcode.com/2021/day/7
"""
from typing import List

from ..tools import relative_to_file, load_input

DAY = 7
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT = """16,1,2,0,4,2,7,1,2,14"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)

def parse_input(s: str) -> List[int]:
    data = sorted([int(v) for v in s.split(",")])
    print(f"Loaded positions of {len(data)} crabs.")
    return data


# -- Part 1 -------------------------------------------------------------------

def median(l: List[int]) -> int:
    """Determines the median value of a list of integers

    For lists with even-numbered length, the central values are averaged, then
    rounded to the *nearest* integer.
    """
    l = sorted(l)  # ensuring it's sorted
    N = len(l)

    if N % 2 == 1:
        return l[N//2]
    return round((l[N//2 - 1] + l[N//2])/2)


def solve_part1(*, input_mode: str) -> int:
    """Computes the solution for part 1"""
    positions = parse_input(load_input(input_mode, **INPUT_KWARGS)[0])
    if input_mode == "test":
        print(positions)

    target_pos = median(positions)
    print(f"Target position (median value):  {target_pos}")

    fuel_consumption = sum([abs(x-target_pos) for x in positions])
    return fuel_consumption


# -- Part 2 -------------------------------------------------------------------

def solve_part2(*, input_mode: str, dx: int = 10) -> int:
    """Computes the solution for part 2"""
    def compute_fuel_consumption(positions: List[int], target: int) -> int:
        return sum(
            sum(n for n in range(abs(x-target) + 1)) for x in positions
        )

    positions = parse_input(load_input(input_mode, **INPUT_KWARGS)[0])
    if input_mode == "test":
        print(positions)

    # Look around the mean position for smallest values
    mean_pos = round(sum(positions)/len(positions))
    print(f"Mean position:  {mean_pos}\n")

    test_target = [t for t in range(mean_pos - dx, mean_pos + dx + 1)]
    test_fuel = [compute_fuel_consumption(positions, t) for t in test_target]

    for _target, _fuel in zip(test_target, test_fuel):
        print(f"target {_target:3d} : {_fuel}")

    target_pos = test_target[test_fuel.index(min(test_fuel))]

    print(
        f"Smallest fuel consumption (for target positions {mean_pos} ± {dx}) "
        f"at:  {target_pos}"
    )
    return compute_fuel_consumption(positions, target_pos)
    

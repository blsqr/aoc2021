"""Solution for Day 6: Lanternfish

For puzzle text, see: https://adventofcode.com/2021/day/6
"""
from typing import List

from ..tools import relative_to_file, load_input

DAY = 6
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT = """3,4,3,1,2"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)

def parse_input(data: str) -> List[int]:
    return [int(v) for v in data.split(",")]


def procreate_lanternfish_naive(ages: List[int]) -> List[int]:
    """Simulates procreation of lanternfish from their age list ... which does
    not scale particularly well.
    """
    # Decrement ages
    ages = [age - 1 for age in ages]

    # Add offspring to back of list
    ages += [8] * ages.count(-1)

    # Reset ages to 6 for those that produced offspring (have age == -1)
    ages = [age if age >= 0 else 6 for age in ages]
    return ages

def procreate_lanternfish_age_distribution(distr: List[int]) -> List[int]:
    """Uses the age distribution for simulating procreation"""
    # Determine number of procreating offspring
    num_procreating = num_offspring = distr[0]

    # Shift distribution left (equal to decrementing all ages) and add
    # offspring age bracket on the right side
    distr = distr[1:] + [num_procreating]

    # Add those that were previously in bracket 0 to bracket 6
    distr[6] += num_procreating
    return distr


# -- Part 1 -------------------------------------------------------------------

def solve_part1(*, input_mode: str, days: int = 80) -> int:
    """Computes the solution for part 1"""
    data = load_input(input_mode, **INPUT_KWARGS)
    ages = parse_input(data[0])  # single line

    print(f"Initial state: {len(ages)} fish {ages if len(ages) < 30 else ''}")
    for day in range(1, days+1):
        ages = procreate_lanternfish_naive(ages)
        print(
            f"After day {day:2d}:  {len(ages)} fish "
            f"{ages if len(ages) < 30 else ''}"
        )

    return len(ages)


# -- Part 2 -------------------------------------------------------------------

def solve_part2(*, input_mode: str, days: int = 256) -> int:
    """Computes the solution for part 2"""
    data = load_input(input_mode, **INPUT_KWARGS)
    ages = parse_input(data[0])  # single line

    # Create an age distribution list
    age_distr = [ages.count(n) for n in range(9)]


    print(f"Initial state: {sum(age_distr)} fish ({age_distr})")
    for day in range(1, days+1):
        age_distr = procreate_lanternfish_age_distribution(age_distr)
        print(f"After day {day:2d}:  {sum(age_distr)} fish ({age_distr})")

    return sum(age_distr)
    

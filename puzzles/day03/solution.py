"""Solution for Day 3: Binary Diagnostic

For puzzle text, see: https://adventofcode.com/2021/day/3
"""

from typing import Callable, List

import numpy as np

from ..tools import relative_to_file, load_input

DAY = 3
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT = """
    00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010
"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)


# -- Part 1 -------------------------------------------------------------------

def bin2dec(binary_num: List[int]) -> int:
    """Converts a binary number to a decimal.

    Args:
        binary_num (List[int]): Binary number as list of integer numbers.
    """
    dec = 0
    for n, bit in enumerate(binary_num[::-1]):
        dec += bool(bit) * 2**n

    return dec

def solve_part1(*, input_mode: str):
    """Computes the solution for part 1"""
    data = load_input(input_mode, **INPUT_KWARGS)

    # Generate list of lists with boolean data type, which can then be turned
    # into a 2D array, allowing easier manipulation of column data
    #   axis 0: selects rows
    #   axis 1: selects column
    arr = np.array([[c == "1" for c in line] for line in data])
    n_rows, n_cols = arr.shape
    print(f"Data has {n_rows} lines and {n_cols} columns.")

    # Compute the sum over each column and check against undefined behaviour
    arr_reduced = np.sum(arr, axis=0)
    print(f"  Number of 0 bits: {n_rows - arr_reduced}")
    print(f"  Number of 1 bits: {arr_reduced}")

    if n_rows % 2 == 0 and np.any(arr_reduced == n_rows//2):
        raise ValueError(
            "Got equal number of 0 and 1 bits in at least one of the columns, "
            f"which is undefined behaviour!\nNumber of 1 bits:  {arr_reduced}"
        )

    # Compute gamma (most common bit) and epsilon (least common bit)
    gamma_bin = (arr_reduced > n_rows // 2).astype(int)
    epsilon_bin = (arr_reduced < n_rows // 2).astype(int)

    gamma_dec = bin2dec(gamma_bin)
    epsilon_dec = bin2dec(epsilon_bin)

    print(f"Gamma:    {gamma_bin}  -->  {gamma_dec}")
    print(f"Epsilon:  {epsilon_bin}  -->  {epsilon_dec}")

    return gamma_dec * epsilon_dec


# -- Part 2 -------------------------------------------------------------------

def filter_by_bit_criteria(
    candidates: list, bit_pos: int, op: Callable
) -> list:
    """Filter the candidates list by the bit criteria for a certain position"""
    n1 = sum([c[bit_pos] == "1" for c in candidates])
    n0 = len(candidates) - n1
    keep_bit = "1" if op(n0, n1) else "0"
    print(
        f"{len(candidates):4d} candidates, bit position {bit_pos:2d}:  "
        f"{n0:3d} x0, {n1:3d} x1  =>  keep {keep_bit}"
    )

    filtered = [c for c in candidates if c[bit_pos] == keep_bit]
    return filtered


def apply_filter(candidates: list, op: Callable) -> bin:
    """Applies the filter to the list of candidate bit patterns

    Args:
        candidates (list): List of binary number strings
        op (Callable): The binary comparison operator to determine by
            which bit to filter, i.e. the candidate bit patterns with which
            bit in the currently selected bit position to keep.
            The operator is called with arguments (# bit 0, # bit 1) and the
            return value (true or false) determines which bit patterns (with a
            1 or 0 in the position) will be kept.
    """
    col = 0
    while len(candidates) > 1:
        candidates = filter_by_bit_criteria(candidates, bit_pos=col, op=op)
        col += 1

    else:
        print("Gotcha!\n")
        return candidates[0]


def solve_part2(*, input_mode: str):
    """Computes the solution for part 2"""
    data = load_input(input_mode, **INPUT_KWARGS)
    print(f"Data has {len(data)} lines with {len(data[0])} columns.\n")

    o2gen_bin = apply_filter(
        [d for d in data], op=lambda n0, n1: n0 <= n1,
    )
    co2scrub_bin = apply_filter(
        [d for d in data], op=lambda n0, n1: n0 > n1,
    )

    o2gen_dec = int(o2gen_bin, 2)
    co2scrub_dec = int(co2scrub_bin, 2)

    print(f"O2 generator:  {o2gen_bin}  -->  {o2gen_dec}")
    print(f"CO2 scrubber:  {co2scrub_bin}  -->  {co2scrub_dec}")

    return o2gen_dec * co2scrub_dec
    

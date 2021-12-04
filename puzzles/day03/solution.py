"""Solution for Day 3: Binary Diagnostic

For puzzle text, see: https://adventofcode.com/2021/day/3
"""

import numpy as np

from ..tools import relative_to_file, load_input, bin2dec

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

def solve_part2(*, input_mode: str):
    """Computes the solution for part 2"""
    data = load_input(input_mode, **INPUT_KWARGS)

    raise NotImplementedError()
    

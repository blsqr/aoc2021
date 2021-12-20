"""Solution for Day 13: Transparent Origami

For puzzle text, see: https://adventofcode.com/2021/day/13
"""
import numpy as np

from ..tools import relative_to_file, load_input

DAY = 13
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)


def parse_input(lines: list) -> tuple:
    """Parses the input to an np.ndarray and a list of folding instructions"""
    dots = []
    x_max, y_max = 0, 0
    axis_map = dict(x=0, y=1)
    fold_instr = []

    for line in lines:
        if line.startswith("fold along"):
            direction, value = line.split("=")
            fold_instr.append(
                (direction[-1], axis_map[direction[-1]], int(value))
            )
            continue

        elif not line:
            continue

        x, y = line.split(",")
        x, y = int(x), int(y)
        dots.append((x, y))
        x_max = max(x_max, x)
        y_max = max(y_max, y)

    # Make sure array dimensions will be odd
    x_max += 1
    y_max += 1
    x_max = x_max + 1 if x_max % 2 == 0 else x_max
    y_max = y_max + 1 if y_max % 2 == 0 else y_max

    arr = np.zeros((x_max, y_max), dtype=bool)
    for x, y in dots:
        arr[x,y] = True

    return arr, fold_instr


# -- Part 1 -------------------------------------------------------------------

print_array = lambda arr: print(arr.astype(int).T, end="\n\n")

def fold(arr, *, axis: int, index: int) -> np.ndarray:
    """Folds along the given axis and index, returning a new boolean array"""
    # Helper functions to construct axis-specific selector tuples
    make_axis_tuple = lambda a, b: (a, b) if axis == 0 else (b, a)

    # Construct selectors slices and separate into "lower" and "upper" arrays
    sel_lower = slice(0, index)
    sel_upper = slice(index+1, None)

    lower = arr[make_axis_tuple(sel_lower, Ellipsis)]
    upper = arr[make_axis_tuple(sel_upper, Ellipsis)]

    # Zero-pad them such that they have the same shape
    to_pad = upper.shape[axis] - lower.shape[axis]
    if to_pad > 0:
        # Upper is larger, lower needs padding on low-indexed side
        print("upper", upper.shape, lower.shape)
        upper = np.pad(upper, make_axis_tuple(to_pad, 0),
                       mode="constant", constant_values=0)
        print(upper.shape)

    elif to_pad < 0:
        # Lower is larger, upper needs padding on high-indexed side
        print("lower", lower.shape, upper.shape)
        lower = np.pad(lower, make_axis_tuple(0, -to_pad),
                       mode="constant", constant_values=0)
        print(lower.shape)

    # Combine
    return lower | np.flip(upper, axis=axis)


def solve_part1(*, input_mode: str) -> int:
    """Computes the solution for part 1"""
    data = load_input(input_mode, **INPUT_KWARGS)
    arr, instr = parse_input(data)
    print(f"Got paper of size {arr.shape} and {len(instr)} fold instructions:")
    print_array(arr)

    # Only apply the first instruction
    print("Only applying first instruction ...")
    _, axis, index = instr[0]
    arr = fold(arr, axis=axis, index=index)
    print(f"Now have {np.sum(arr)} dots visible:")
    print_array(arr)

    return np.sum(arr)




# -- Part 2 -------------------------------------------------------------------

def solve_part2(*, input_mode: str) -> int:
    """Computes the solution for part 2"""
    data = load_input(input_mode, **INPUT_KWARGS)
    arr, instr = parse_input(data)
    print(f"Got paper of size {arr.shape} and {len(instr)} fold instructions:")
    print_array(arr)

    for n, (direction, axis, index) in enumerate(instr):
        print(f"Instruction {n+1}:  Fold along {direction}={index} ... "
              f"paper shape: {arr.shape}")
        arr = fold(arr, axis=axis, index=index)
        print(f"Now have {np.sum(arr)} dots visible:")
        print_array(arr)
    

    print("Final display:\n")
    for line in arr.T:
        print("".join("#" if v else " " for v in line))

    return "(see above)"

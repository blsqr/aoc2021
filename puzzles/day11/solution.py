"""Solution for Day 11: Dumbo Octopus

For puzzle text, see: https://adventofcode.com/2021/day/11
"""
import numpy as np

from ..tools import relative_to_file, load_input

DAY = 11
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)


# -- Part 1 -------------------------------------------------------------------

def evaluate_flashes(energy: np.ndarray, has_flashed: np.ndarray) -> int:
    """Evaluates flashes of the Dumbo Octopusses and returns the number of new
    flashes that occured as a result.
    """
    # Mark as flashed and set energy to zero for those that have flashed
    new_flashes = energy > 9
    energy[new_flashes] = 0
    has_flashed[new_flashes] = True

    delta_energy = np.zeros_like(energy)
    y_max, x_max = energy.shape

    # Propagate energy to Moore neighbours
    it = np.nditer(new_flashes, flags=['multi_index'])
    for flashed in it:
        if not flashed:
            continue

        # Construct a 3x3 subarray selector and mark the whole neighbourhood
        # (including the source of the flash) as being in flash vicinity,
        # incrementing the energy change. Then discount the central point's
        # energy change, because that one is not affected
        y, x = it.multi_index
        sel = (
            slice(max(0, y-1), min(y+2, y_max)),
            slice(max(0, x-1), min(x+2, x_max)),
        )
        delta_energy[sel] += 1
        delta_energy[y, x] -= 1

    # print(f"\nnew_flashes:\n{new_flashes.astype(int)}")
    # print(f"\ndelta_energy:\n{delta_energy.astype(int)}")
    # print(f"\ndelta_energy & ~has_flashed:\n{(delta_energy & ~has_flashed).astype(int)}")
    # Can now increment those areas that are in vicinity but have not flashed.
    # Flash evaluation will occur in next call of this function
    energy += delta_energy

    return np.sum(new_flashes)

def solve_part1(*, input_mode: str) -> int:
    """Computes the solution for part 1"""
    data = load_input(input_mode, **INPUT_KWARGS)
    energy = np.array([[int(v) for v in line] for line in data])
    has_flashed = np.zeros_like(energy, dtype=bool)
    print(
        f"Have Dumbo Octopus energy map of shape {energy.shape}:\n{energy}\n"
    )

    num_flashes = 0
    num_new_flashes = None
    num_steps = 100 #if input_mode != "test" else 3

    for n in range(1, num_steps + 1):
        energy += 1
        num_new_flashes = None
        has_flashed.fill(False)

        while num_new_flashes != 0:
            num_new_flashes = evaluate_flashes(energy, has_flashed)
            num_flashes += num_new_flashes

        energy[has_flashed] = 0
        print(
            f"After step {n:3d}:  {num_flashes:3d} flashes so far\n{energy}\n"
        )

    return num_flashes


# -- Part 2 -------------------------------------------------------------------

def solve_part2(*, input_mode: str) -> int:
    """Computes the solution for part 2"""
    data = load_input(input_mode, **INPUT_KWARGS)
    raise NotImplementedError()
    

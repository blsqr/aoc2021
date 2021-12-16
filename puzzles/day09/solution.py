"""Solution for Day 9: Smoke Basin

For puzzle text, see: https://adventofcode.com/2021/day/9
"""
from collections import defaultdict

import numpy as np

from ..tools import relative_to_file, load_input

DAY = 9
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)

PAD_CONSTANT = 9

# -- Part 1 -------------------------------------------------------------------

def find_low_points(hmap: np.ndarray) -> list:
    """Returns a list of (y, x) coordinates of low points in the height map"""
    print("Looking for low points ...")

    # Add padding to avoid needing boundary checks
    print("  Adding padding ...")
    hmap = np.pad(hmap, 1, mode="constant", constant_values=PAD_CONSTANT)

    # ... just iterate and check (von Neumann) neighbours
    low_points = []  # (y, x) coordinate tuples

    it = np.nditer(hmap, flags=['multi_index'])
    for h in it:
        if h == PAD_CONSTANT:
            # Don't need to check the padding
            continue

        y, x = it.multi_index
        if min(hmap[y, x+1], hmap[y, x-1], hmap[y+1, x], hmap[y-1, x]) > h:
            low_points.append((y-1, x-1))  # -1 to counteract padding

    print(f"  Found {len(low_points)} low points.")
    return low_points

def solve_part1(*, input_mode: str) -> int:
    """Computes the solution for part 1 by simply looking at the neighbours"""
    data = load_input(input_mode, **INPUT_KWARGS)
    hmap = np.array([[int(v) for v in l] for l in data])
    print(f"Have height map of shape {hmap.shape}.")

    low_points = find_low_points(hmap)

    if input_mode == "test":
        print(
            "\n".join(f"    ({x}, {y}) : {hmap[y, x]}" for y, x in low_points)
        )
        print(f"\nHeight map:\n{hmap}")

    return sum(hmap[y,x] + 1 for y, x in low_points)


# -- Part 2 -------------------------------------------------------------------

def mark_cc(mask, clusters, *, midx: tuple, cluster_id: int):
    """Recursively marks all neighbours of the given ``midx`` position that are
    part of the same component with the given cluster ID
    """
    # If it's a boundary or there already is an ID, there's nothing to do
    if not mask[midx] or clusters[midx]:
        return

    # Otherwise: mark and recurse
    clusters[midx] = cluster_id
    y, x = midx
    mark_cc(mask, clusters, midx=(y-1, x), cluster_id=cluster_id)
    mark_cc(mask, clusters, midx=(y+1, x), cluster_id=cluster_id)
    mark_cc(mask, clusters, midx=(y, x-1), cluster_id=cluster_id)
    mark_cc(mask, clusters, midx=(y, x+1), cluster_id=cluster_id)

def find_connected_components(mask: np.ndarray) -> list:
    """Given a boolean mask, finds the connected components and returns a list
    of sets, each set representing the coordinates of the connected positions
    in the mask.

    .. note::

        This relies on the mask being padded with False values.
    """
    clusters = np.zeros_like(mask, dtype=int)

    # Recursively walk through the mask and associate positions with an ID
    it = np.nditer(mask, flags=['multi_index'])
    for start_id, val in enumerate(it):
        if not val:
            # Is a boundary, nothing to mark
            continue
        # else: is part of a basin
        # Recursively mark neighbours with an (arbitrary) ID
        mark_cc(mask, clusters, midx=it.multi_index, cluster_id=start_id)

    print(f"Clusters:\n{clusters}")

    # Gather clusters
    cc = defaultdict(set)
    it = np.nditer(clusters, flags=['multi_index'])
    for cluster_id in it:
        if not cluster_id:
            continue
        cc[int(cluster_id)].add(tuple(it.multi_index))

    return list(cc.values())

def solve_part2(*, input_mode: str) -> int:
    """Computes the solution for part 2 using a 'watershed' method"""
    data = load_input(input_mode, **INPUT_KWARGS)
    hmap = np.array([[int(v) for v in l] for l in data])
    print(f"Have height map of shape {hmap.shape}.")

    # Again add a padding to avoid boundary problems
    hmap = np.pad(hmap, 1, mode="constant", constant_values=PAD_CONSTANT)

    # Mark basins
    hmap_mask = hmap < 9
    if input_mode == "test":
        print(f"Height map (padded):\n{hmap}\n")
        print(f"Basins:\n{hmap_mask.astype(int)}\n")

    # Find connected components by walking
    cc = find_connected_components(hmap_mask)
    print(f"Found {len(cc)} connected components.")
    cc_sizes_desc = sorted([len(c) for c in cc])[::-1]  # --> descending size

    return cc_sizes_desc[0] * cc_sizes_desc[1] * cc_sizes_desc[2]

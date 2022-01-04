"""Solution for Day 15: Chiton

For puzzle text, see: https://adventofcode.com/2021/day/15
"""
import itertools

import numpy as np
import numpy.ma as ma

from ..tools import relative_to_file, load_input

DAY = 15
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)


def shortest_path_on_array(w: np.ndarray, *, start, end) -> tuple:
    """A Dijkstra shortest-path search on an array (i.e.: directed graph
    without edge weights and only node weights)

    This is certainly not the most efficient implementation as it is not based
    on a priority queue but searches the smallest distance on the whole array
    of distances.
    """
    if w.ndim != 2:
        # NOTE To generalise, adapt neighbourhood implementation
        raise ValueError(f"Expected 2D array, got {w.ndim}-dimensional one!")

    distance = ma.MaskedArray(np.full_like(w, np.inf, dtype=float), mask=False)
    prev = np.full_like(w, None, dtype=object)

    distance[start] = 0

    while np.sum(distance.mask) < w.size:
        # Find unvisited node with lowest distance and mark as visited
        u = np.unravel_index(
            distance.argmin(fill_value=np.inf), distance.shape
        )
        distance[u] = ma.masked

        # Was the target node reached?
        if u == end:
            break

        # Iterate over neighbors that were not visited yet
        uy, ux = u
        for nb in (
            (uy-1, ux),
            (uy+1, ux),
            (uy, ux-1),
            (uy, ux+1),
        ):
            # Check for boundary (to avoid index errors) and skip visited nodes
            nby, nbx = nb
            if not ((0 <= nby < w.shape[0]) and (0 <= nbx < w.shape[1])):
                continue

            if distance.mask[nb]:
                continue

            # Potentially update distances and predecessors
            alt = distance.data[u] + w[nb]
            if alt < distance[nb]:
                distance[nb] = alt
                prev[nb] = u

    return distance.data, prev


def mark_path(prev: np.ndarray, *, last: tuple) -> tuple:
    """Follows the path through an object array, beginning at the last entry.
    The path is marked in a boolean array.

    Returns (path array, step count)
    """
    path = np.zeros_like(prev, dtype=bool)
    path[last] = True

    u = prev[last]
    steps = 0
    while prev[u] is not None:
        path[u] = True
        u = prev[u]
        steps += 1
    path[u] = True

    return path, steps

# -- Part 1 -------------------------------------------------------------------

def solve_part1(*, input_mode: str) -> int:
    """Computes the solution for part 1"""
    data = load_input(input_mode, **INPUT_KWARGS)
    nw = np.array([[int(v) for v in line] for line in data])
    print(f"Have risk level map of shape {nw.shape}")
    if input_mode == "test":
        print(nw)

    start = (0, 0)
    end = (nw.shape[0]-1, nw.shape[1]-1)
    print(
        f"Looking for path with lowest total risk from {start} to {end} ..."
    )
    distance, prev = shortest_path_on_array(nw, start=start, end=end)

    return int(distance[end])


# -- Part 2 -------------------------------------------------------------------

def solve_part2(*, input_mode: str) -> int:
    """Computes the solution for part 2"""
    data = load_input(input_mode, **INPUT_KWARGS)

    # Construct 5x5 tiled risk map with risk levels incremented depending on
    # position on the tile
    nw = np.array([[int(v) for v in line] for line in data])
    tiles = (5, 5)
    tile_size_y, tile_size_x = nw.shape
    nw = np.tile(nw, tiles)

    for tile_y, tile_x in itertools.product(range(tiles[0]), range(tiles[1])):
        sel = (
            slice(tile_y * tile_size_y, (tile_y + 1) * tile_size_y),
            slice(tile_x * tile_size_x, (tile_x + 1) * tile_size_x),
        )

        # Increment risk level depending on distance
        nw[sel] += tile_y + tile_x

        # Let 9 wrap back around to 1
        nw[nw >= 10] -= 9

    print(f"Have tiled risk level map of shape {nw.shape}")

    # Can now compute the shortest path in the same way as above
    start = (0, 0)
    end = (nw.shape[0]-1, nw.shape[1]-1)
    print(
        f"Looking for path with lowest total risk from {start} to {end} ..."
    )
    distance, prev = shortest_path_on_array(nw, start=start, end=end)

    if input_mode == "test":
        path, step_count = mark_path(prev, last=end)
        for y, line in enumerate(path):
            for x, is_on_path in enumerate(line):
                print("#" if is_on_path else ".", end="")
                # print(nw[y,x] if is_on_path else ".", end="")
                # print("." if is_on_path else nw[y,x], end="")
            print("")

    return int(distance[end])
    

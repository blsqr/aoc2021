"""Solution for Day 15: Chiton

For puzzle text, see: https://adventofcode.com/2021/day/15
"""
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


# -- Part 1 -------------------------------------------------------------------

def shortest_path_on_array(w: np.ndarray, *, start, end):
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
    raise NotImplementedError()
    

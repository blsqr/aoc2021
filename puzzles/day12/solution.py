"""Solution for Day 12: Passage Pathing

For puzzle text, see: https://adventofcode.com/2021/day/12
"""
import copy
from collections import defaultdict

from ..tools import relative_to_file, load_input

DAY = 12
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT_SMALL = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

TEST_INPUT_MEDIUM = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""

TEST_INPUT_LARGE = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""

TEST_INPUT = TEST_INPUT_SMALL

INPUT_KWARGS = dict(
    day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT_LARGE,
    test_inputs=dict(
        small=TEST_INPUT_SMALL,
        medium=TEST_INPUT_MEDIUM,
        large=TEST_INPUT_LARGE,
    ),
)

is_small_cave = lambda cave: cave.islower()

def construct_network(links: list) -> dict:
    """Constructs an undirected network from a list of links"""
    network = defaultdict(set)
    for start, end in links:
        network[start].add(end)
        network[end].add(start)

    return network

def walk_network(
    nw: dict, *, position: str, visited: list, paths: set,
    start: str = "start", end: str = "end",
    small_cave_dual_visit: bool = False,
) -> None:
    """"""
    # Can we move to this position?
    if is_small_cave(position):
        if not small_cave_dual_visit and position in visited:
            # Cannot continue
            return

        elif small_cave_dual_visit:
            if visited and position == start:
                # May not go back to the start
                return

            # Was the dual visit already done?
            elif position in visited:
                # Can continue, but no further dual visit is allowed
                small_cave_dual_visit = False

        # else: may move to this position

    # Keep track of where we are now
    visited.append(position)

    # Reached destination?
    if position == end:
        paths.add(tuple(visited))
        return

    # Branch into all possible directions
    for target in nw[position]:
        walk_network(
            nw,
            position=target,
            visited=copy.copy(visited),
            paths=paths,
            start=start,
            end=end,
            small_cave_dual_visit=small_cave_dual_visit
        )


# -- Part 1 -------------------------------------------------------------------

def solve_part1(*, input_mode: str) -> int:
    """Computes the solution for part 1"""
    data = load_input(input_mode, **INPUT_KWARGS)
    links = [line.split("-") for line in data]
    print(f"Have network with {len(links)} links. Now walking ...")

    paths = set()
    walk_network(
        construct_network(links),
        position="start",
        visited=[],
        paths=paths,
        start="start",
        end="end",
    )
    print(f"Found {len(paths)} unique paths through the cave network.")

    return len(paths)


# -- Part 2 -------------------------------------------------------------------

def solve_part2(*, input_mode: str) -> int:
    """Computes the solution for part 2"""
    data = load_input(input_mode, **INPUT_KWARGS)
    links = [line.split("-") for line in data]
    print(f"Have network with {len(links)} links. Now walking ...")

    paths = set()
    walk_network(
        construct_network(links),
        position="start",
        visited=[],
        paths=paths,
        start="start",
        end="end",
        small_cave_dual_visit=True,
    )
    print(f"Found {len(paths)} unique paths through the cave network.")

    return len(paths)
    

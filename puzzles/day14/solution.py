"""Solution for Day 14: Extended Polymerization

For puzzle text, see: https://adventofcode.com/2021/day/14
"""
from collections import Counter, defaultdict

from ..tools import relative_to_file, load_input

DAY = 14
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)


# -- Part 1 -------------------------------------------------------------------

def apply_rules(polymer: list, *, rules: dict) -> None:
    # Determine insertions
    insertions = []
    for i, (p1, p2) in enumerate(zip(polymer[:-1], polymer[1:])):
        pat = p1 + p2
        try:
            insertions.append((i + len(insertions) + 1, rules[pat]))
        except KeyError:
            pass

    # ... and apply them
    for insertion in insertions:
        polymer.insert(*insertion)


def solve_part1(*, input_mode: str, N: int = 10) -> int:
    """Computes the solution for part 1"""
    data = load_input(input_mode, **INPUT_KWARGS)
    polymer = list(data[0])
    rules = dict(rule.split(" -> ") for rule in data[2:])

    for n in range(N):
        apply_rules(polymer, rules=rules)
        print(f"After step {n+1:2d}:  polymer length is {len(polymer)}")
        print("".join(polymer))

    print(f"Final polymer:\n{''.join(polymer)}\n")

    letters = Counter(polymer).most_common()  # (letter, count) pairs
    print("\nLetter counts:", letters)
    _, most_common = letters[0]
    _, least_common = letters[-1]
    return most_common - least_common



# -- Part 2 -------------------------------------------------------------------

def solve_part2(*, input_mode: str, N: int = 40) -> int:
    """Computes the solution for part 2"""
    data = load_input(input_mode, **INPUT_KWARGS)
    polymer = list(data[0])
    rules = dict(rule.split(" -> ") for rule in data[2:])

    # Cannot brute-force this one ... keep track of pair occurences instead
    pairs = defaultdict(int)
    for p1, p2 in zip(polymer[:-1], polymer[1:]):
        pairs[p1+p2] += 1

    # Now perform the iterations on the pair counters, not the polymer itself
    for n in range(N):
        print(f"Applying step {n+1:2d} ... ", end="")
        changes = list()

        for pair, count in pairs.items():
            for pat, ins in rules.items():
                if pat != pair:
                    continue

                # Got a match, keep track of them (to not invalidate iterator)
                changes.append((pair,           -count))
                changes.append((pair[0] + ins,  +count))
                changes.append((ins + pair[1],  +count))

        # Apply changes
        for pair, delta in changes:
            pairs[pair] += delta

        print(f"polymer length is {sum(v for v in pairs.values()) + 1} now.")

    letters = defaultdict(int)
    for (p1, p2), n in pairs.items():
        letters[p1] += n
        letters[p2] += n

    # Correct letter counts:
    #   - First two positions have not been counted twice
    #   - With all positions having been counted twice, can divide by two
    letters[polymer[0]] += 1
    letters[polymer[-1]] += 1
    letters = {k: v//2 for k, v in letters.items()}

    letters = sorted((v, k) for k, v in letters.items())[::-1]
    print("\nLetter counts:", letters)
    most_common, _ = letters[0]
    least_common, _ = letters[-1]
    return most_common - least_common

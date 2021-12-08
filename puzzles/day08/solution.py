"""Solution for Day 8: Seven Segment Search

For puzzle text, see: https://adventofcode.com/2021/day/8
"""
from typing import Dict, List

from ..tools import relative_to_file, load_input

DAY = 8
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT_SINGLE = """
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
"""
TEST_INPUT = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)

EASY_DIGITS = {    # digit -> #segments
    1: 2,
    4: 4,
    7: 3,
    8: 7,
}
EASY_PATTERNS = {  # #segments -> digit
    2: 1,
    4: 4,
    3: 7,
    7: 8,
}

# -- Part 1 -------------------------------------------------------------------

def solve_part1(*, input_mode: str) -> int:
    """Computes the solution for part 1"""
    data = load_input(input_mode, **INPUT_KWARGS)

    all_outputs = [l.split("|")[1].split() for l in data]
    return sum(
        sum(
            len(output) in EASY_DIGITS.values() for output in outputs
        ) for outputs in all_outputs
    )


# -- Part 2 -------------------------------------------------------------------

def item(s):
    """Returns the only element from a container, raises otherwise"""
    s = list(s)
    if len(s) != 1:
        raise ValueError(f"Given object has {len(s)} != 1 items! {s}")
    return s[0]

def determine_encoding(
    patterns: List[List[str]], *, verbose: bool
) -> Dict[str, int]:
    """Determines the mapping from patterns to digits"""
    # Easy digits first
    encoding = {
        pattern: EASY_PATTERNS.get(len(pattern)) for pattern in patterns
    }

    # Function to get the inverse encoding as a set
    def get_pattern(digit: int) -> set:
        candidates = [pat for pat, dig in encoding.items() if dig == digit]
        if len(candidates) != 1:
            raise ValueError(
                f"No (or no unambiguous) pattern found for digit {digit}!"
            )
        return set(candidates[0])

    # Start deducing patterns using set operations
    #   & : intersection
    #   | : union
    #   - : difference
    #   ^ : symmetric difference

    # - Digit 3 is the 5-segment pattern with overlap to 1 of 2:
    #   Both 5 and 2 only have an overlap of 1. Notation:
    #   #(3 & 1) = 2
    #
    #   The remaining 5-segment patterns differ in their overlap to 4:
    #   #(5 & 4) = 3
    #   #(2 & 4) = 2
    pat3 = item(
        p for p in patterns
        if len(p) == 5 and len(set(p) & get_pattern(1)) == 2
    )
    pat5 = item(
        p for p in patterns
        if len(p) == 5 and p != pat3 and len(set(p) & get_pattern(4)) == 3
    )
    pat2 = item(
        p for p in patterns if len(p) == 5 and p not in (pat3, pat5)
    )

    encoding[pat3] = 3
    encoding[pat5] = 5
    encoding[pat2] = 2

    # - Among the 6-segment patterns, the overlap is as follows
    #   #(6 & 1) = 1
    #   #(9 & 1) = 2
    #   #(0 & 1) = 2
    #
    #   #(9 & 3) = 5
    #   #(0 & 3) = 4
    pat6 = item(
        p for p in patterns
        if len(p) == 6 and len(set(p) & get_pattern(1)) == 1
    )
    pat9 = item(
        p for p in patterns
        if len(p) == 6 and p != pat6 and len(set(p) & get_pattern(3)) == 5
    )
    pat0 = item(
        p for p in patterns if len(p) == 6 and p not in (pat6, pat9)
    )

    encoding[pat6] = 6
    encoding[pat9] = 9
    encoding[pat0] = 0

    if verbose:
        _fmt = lambda pat: f"{pat if pat is not None else '':>7}"
        print(f"Patterns:  {' '.join(_fmt(pat) for pat in patterns)}")
        print(f"Encoding:  {' '.join(_fmt(v) for v in encoding.values())}")

    return encoding


def decode(outputs, *, encoding: Dict[str, int], verbose: bool) -> int:
    """Decodes a list of output patterns to an integer"""
    res = int("".join(str(encoding[pat]) for pat in outputs))
    if verbose:
        print(f"Decoding output ...  {' '.join(outputs)}  ==>  {res}\n")

    return res


def solve_part2(*, input_mode: str) -> int:
    """Computes the solution for part 2"""
    verbose = (input_mode == "test")
    data = load_input(input_mode, **INPUT_KWARGS)

    sort = lambda pat: "".join(sorted(pat))
    all_patterns = [[sort(p) for p in l.split("|")[0].split()] for l in data]
    all_outputs = [[sort(p) for p in l.split("|")[1].split()] for l in data]

    all_decoded_outputs = []

    for patterns, outputs in zip(all_patterns, all_outputs):
        encoding = determine_encoding(patterns, verbose=verbose)
        all_decoded_outputs.append(
            decode(outputs, encoding=encoding, verbose=verbose)
        )

    return sum(all_decoded_outputs)

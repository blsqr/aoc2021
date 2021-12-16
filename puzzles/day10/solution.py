"""Solution for Day 10: Syntax Scoring

For puzzle text, see: https://adventofcode.com/2021/day/10
"""

from ..tools import relative_to_file, load_input

DAY = 10
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)

BRACE_PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
BRACE_PAIRS_INV = {v: k for k, v in BRACE_PAIRS.items()}


def check_syntax(data: list, *, incl_completions: bool = False) -> dict:
    """Performs the syntax check and categorises lines into groups"""
    is_opening = lambda c: c in BRACE_PAIRS.keys()
    is_closing = lambda c: c in BRACE_PAIRS.values()

    invalid_chars = []
    incomplete_lines = []
    valid_lines = []
    corrupted_lines = []
    completions = {}

    for line_no, line in enumerate(data):
        chunks = []

        for n, char in enumerate(line):
            if is_opening(char):
                # Put it on the stack
                chunks.append(char)

            elif is_closing(char):
                if chunks[-1] == BRACE_PAIRS_INV[char]:
                    # Matches its counterpart, can pop it from the stack
                    chunks.pop()

                else:
                    # Invalid closing character. Keep track of it.
                    print(
                        f"Syntax error in line {line_no:3d}, col {n:3d}:  "
                        f"Expected '{BRACE_PAIRS[chunks[-1]]}', got '{char}'"
                    )
                    invalid_chars.append(char)
                    corrupted_lines.append(line_no)
                    break

            else:
                print(
                    f"Syntax error in line {line_no:3d}, col {n:3d}:  "
                    f"Invalid character '{char}'!"
                )

        else:
            # End of line reached, check if it was complete
            if not len(chunks):
                valid_lines.append(line_no)
                continue

            # else: was incomplete
            print(
                f"Syntax error in line {line_no:3d}, col {n:3d}:  "
                f"Incomplete line."
            )
            incomplete_lines.append(line_no)
            if incl_completions:
                completions[line_no] = "".join(
                    BRACE_PAIRS[c] for c in chunks[::-1]
                )

    print(
        f"\nScanned syntax of {len(data)} lines:\n"
        f"  Valid lines:        {valid_lines}\n"
        f"  Incomplete lines:   {incomplete_lines}\n"
        f"  Corrupted lines:    {corrupted_lines}\n"
        f"  Invalid characters: {invalid_chars}\n"
    )

    return dict(
        valid=valid_lines,
        incomplete=incomplete_lines,
        corrupted=corrupted_lines,
        invalid_chars=invalid_chars,
        completions=completions,
    )


# -- Part 1 -------------------------------------------------------------------

def solve_part1(*, input_mode: str) -> int:
    """Computes the solution for part 1"""
    data = load_input(input_mode, **INPUT_KWARGS)
    results = check_syntax(data)

    SCORES = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    return sum(SCORES[char] for char in results["invalid_chars"])


# -- Part 2 -------------------------------------------------------------------

def solve_part2(*, input_mode: str) -> int:
    """Computes the solution for part 2"""
    SCORES = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    def compute_line_score(compl: str):
        s = 0
        for c in compl:
            s = s*5 + SCORES[c]
        return s

    data = load_input(input_mode, **INPUT_KWARGS)
    results = check_syntax(data, incl_completions=True)
    scores = [
        compute_line_score(compl) for compl in results["completions"].values()
    ]
    return sorted(scores)[len(scores)//2]
    

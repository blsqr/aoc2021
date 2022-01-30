"""Provides a CLI for computing puzzle solutions"""

import sys
import importlib
from typing import Callable, Any

import click


# -----------------------------------------------------------------------------

def load_solve_func(day: int, part: int) -> Callable:
    """Loads the solution function for the specified day and part"""
    try:
        module = importlib.import_module(f"puzzles.day{day:02d}.solution")
        return getattr(module, f"solve_part{part:1d}")

    except (ImportError, AttributeError) as err:
        raise ValueError(
            f"There is no solution for day {day}, part {part} available yet! "
            "... or there is a syntax error, see above!"
        ) from err


def check_input_mode(ctx, param, value):
    """Makes sure that input mode has the expected form"""
    if value in ("file", "test") or value.startswith("test:"):
        return value
    raise click.BadParameter(
        f"Expected `file`, `test`, or `test:<key>`, but got '{value}'!"
    )


@click.command(context_settings=dict(help_option_names=("-h", "--help")))
@click.argument("day", type=click.IntRange(1, 25))
@click.argument("part", type=click.IntRange(1, 2))
@click.option(
    "-i", "--input-mode", default="file", callback=check_input_mode,
    help=(
        "Which input mode to use. Can be `file` or `test`. "
        "For test input, can use the format `test:<key>` to select "
        "different kinds of test input, `<key>` depending on the solution."
    )
)
def get_solution(*, day: int, part: int, input_mode: str) -> int:
    """Solves the Advent of Code 2021 puzzle for the selected DAY and PART."""
    print(f"\n--- AoC'21: Day {day:02d}, Part {part} ---\n")
    
    print("Loading solution function ...")
    solve_func = load_solve_func(day, part)

    print("Invoking solution function ...")
    try:
        result = solve_func(input_mode=input_mode.lower())

    except NotImplementedError as err:
        print(f"\nOops, this is not implemented yet! {err}\n")
        sys.exit()

    print(f"\nThe solution is:  {result}\n")
    return result


if __name__ == "__main__":
    get_solution()

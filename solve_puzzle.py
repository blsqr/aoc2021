"""Provides a CLI for computing puzzle solutions"""

import argparse
import importlib
from typing import Callable, Any


def load_solve_func(day: int, part: int) -> Callable:
    """Loads the solution function for the specified day and part"""
    module = importlib.import_module(f"puzzles.day{day:02d}.solution")
    return getattr(module, f"solve_part{part:1d}")


def get_solution(*, day: int, part: int) -> Any:
    """Loads and invokes the solve function for a certain day and solution part
    
    Args:
        day (int): Which day to call the solution of
        part (int): Which part (typically: 1 or 2)
    """
    print(f"\n--- AoC'21: Day {day:02d}, Part {part} ---")
    print("Loading solution function ...")
    solve_func = load_solve_func(day, part)

    print("Now computing solution ...")
    result = solve_func()

    print(f"\nThe solution is:  {result}\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solve Advent of Code 2021 puzzles"
    )
    parser.add_argument(
        "day", type=int, help="Which day to calculate the solution for",
        choices=list(range(1,26)),
    )
    parser.add_argument(
        "part", type=int, help="Which part to calculate the solution for",
        choices=[1, 2]
    )
    args = parser.parse_args()

    get_solution(day=args.day, part=args.part)

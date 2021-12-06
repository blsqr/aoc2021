"""Solution for Day 4: Giant Squid

For puzzle text, see: https://adventofcode.com/2021/day/4
"""
import copy
from typing import Tuple, List

import numpy as np

from ..tools import relative_to_file, load_input

DAY = 4
INPUT_FILE = relative_to_file(__file__, "input.txt")
TEST_INPUT = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

INPUT_KWARGS = dict(day=DAY, fpath=INPUT_FILE, test_input=TEST_INPUT)

BOARD_SIZE = 5


def parse_input(data: list) -> Tuple[List[int], List[np.ndarray]]:
    """Parses the input into a list of bingo numbers to be drawn and a list of
    available bingo boards (as arrays)
    """
    numbers = [int(v) for v in data[0].split(",")]

    current_board = []
    boards = []
    for line in data[2:]:
        if line:
            # Current board needs to be extended by one line
            current_board.append([int(v) for v in line.split()])
        else:
            # Board finished
            boards.append(np.array(current_board))
            current_board = []

    # Need to handle last board separately
    if len(current_board) == BOARD_SIZE:
        boards.append(np.array(current_board))

    return numbers, boards


def mark_boards(
    num: int, *, boards: List[np.ndarray], masks: List[np.ndarray]
) -> None:
    """Marks the corresponding number on the bingo masks (in-place!)"""
    for board, mask in zip(boards, masks):
        mask[board == num] = True


def check_for_bingo(
    *, masks: List[np.ndarray], winners: List[int] = None
) -> Tuple[List[int], int]:
    """Returns the indices of the boards that have a full row or column masked.
    If ``winners`` is given, skips boards with those numbers; this allows to
    keep track of the number in which the winners were found.
    Also returns the change in number of winning boards.
    """
    winners = copy.copy(winners) if winners is not None else []
    num_new_winners = 0

    for board_no, mask in enumerate(masks):
        if board_no in winners:
            # Already know: this is a winner, don't check further
            continue

        for n in range(BOARD_SIZE):
            if all(mask[:,n]) or all(mask[n,:]):
                winners.append(board_no)
                num_new_winners += 1
                break

    return winners, num_new_winners


def print_boards(boards, masks):
    """Prints all boards and masks"""
    print(f"\n--- All {len(boards)} boards ---\n")
    for n, (board, mask) in enumerate(zip(boards, masks)):
        print(f"Board {n}:\n{board}\n{mask}\n")
    print("-"*20)


def score_board(*, drawn_num: int, board: np.ndarray, mask: np.ndarray) -> int:
    """Computes the score for a certain board"""
    print(f"Computing score of board:\n{board}\n\n... with mask:\n{mask}\n")

    sum_unmarked = np.sum(board[~mask])
    print(f"Sum unmarked:  {sum_unmarked},  Last drawn number: {drawn_num}")
    return sum_unmarked * drawn_num



# -- Part 1 -------------------------------------------------------------------

def solve_part1(*, input_mode: str) -> int:
    """Computes the solution for part 1: which board wins first?"""
    data = load_input(input_mode, **INPUT_KWARGS)
    numbers, boards = parse_input(data)
    print(f"Have {len(numbers)} to draw and {len(boards)} bingo boards. "
          "Let's play!")

    # Generate corresponding masks
    #   False:  number not yet selected
    #   True:   number was selected
    masks = [np.zeros_like(board, dtype=bool) for board in boards]

    for n, drawn_num in enumerate(numbers):
        print(f"Draw #{n:<2d}:  {drawn_num:2d}", end="")
        mark_boards(drawn_num, boards=boards, masks=masks)

        winners, _ = check_for_bingo(masks=masks)
        if not winners:
            print("  =>  no Bingo yet")
            continue

        elif len(winners) == 1:
            winner_no = winners[0]
            print(f"  =>  Bingo! on board {winner_no}\n")
            break

        else:
            print(f"  => Bingo! on multiple boards: {winners}")
            raise NotImplementedError("Expected only a single winner ...")

    else:
        raise RuntimeError("No winner!")

    return score_board(
        drawn_num=drawn_num, board=boards[winner_no], mask=masks[winner_no]
    )


# -- Part 2 -------------------------------------------------------------------

def solve_part2(*, input_mode: str) -> int:
    """Computes the solution for part 2: which board wins last?"""
    data = load_input(input_mode, **INPUT_KWARGS)
    numbers, boards = parse_input(data)
    print(f"Have {len(numbers)} to draw and {len(boards)} bingo boards. "
          "Let's play!")

    winners = []
    masks = [np.zeros_like(board, dtype=bool) for board in boards]
    num_boards = len(boards)

    for n, num in enumerate(numbers):
        print(f"Draw #{n:<2d}:  {num:2d}", end="")
        mark_boards(num, boards=boards, masks=masks)

        winners, num_new = check_for_bingo(masks=masks, winners=winners)
        # print_boards(boards, masks)
        if not winners:
            print("  =>  no Bingo yet")
            continue

        elif len(winners) < num_boards:
            print(
                "  =>  Bingo! on "
                f"{len(winners):2d}/{num_boards:<2d} boards (Δ: {num_new})"
            )
            # print(f"  Winners:  {winners}")
            continue

        else:
            last_winner = winners[-1]
            print(
                f"  =>  all Bingo (Δ: {num_new})! "
                f"Last one on board {last_winner}\n"
            )
            # print(f"  Winners:  {winners}")
            break

    else:
        raise RuntimeError("No winner!")

    return score_board(
        drawn_num=num, board=boards[last_winner], mask=masks[last_winner]
    )
    

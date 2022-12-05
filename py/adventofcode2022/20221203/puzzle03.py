#!/usr/bin/python3
# Read the input, find items in both compartments.

import os
import sys


def score_ruck_part1(ruck: str) -> int:
    """Score from splitting the ruck.

    Split the ruck.
    Find overlapping items.
    Sum score from the overlapping items.
    """
    score = 0
    compartment_len = len(ruck) // 2
    c1 = ruck[:compartment_len]
    c2 = ruck[compartment_len:]
    common = (set(c1) & set(c2)).pop()

    # a-z: 1-26
    # A-Z: 27-52
    if common.islower():
        return ord(common) - ord('a') + 1
    return ord(common) - ord('A') + 27


def part1_score(input_filename: str) -> int:
    """Score based on common items in both compartments.

    Find common items by splitting sequence and identifying overlap.
    Score based on rules: a-z = 1-26, A-Z = 27-52.
    """
    score = 0
    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            score += score_ruck_part1(line.strip())

    return score


def part2_score(input_filename: str) -> int:
    """Score based on common items for groups of three lines.

    Find common items by identifying overlap.
    Score still based on rules: a-z = 1-26, A-Z = 27-52.
    """
    score = 0
    with open(input_filename, 'rt') as input_file:
        lines = []
        for line in input_file:
            lines.append(line.strip())
            if len(lines) == 3:
                common = (set(lines[0]) & set(lines[1]) & set(lines[2])).pop()
                if common.islower():
                    score += (ord(common) - ord('a') + 1)
                else:
                    score += (ord(common) - ord('A') + 27)
                lines = []

    return score


def main(argv):
    input_filename = argv[1] if len(argv) > 1 else 'input'
    if not os.path.isfile(input_filename):
        print(f'Error: cannot find file {input_filename}')
        sys.exit(-1)
    print(part1_score(input_filename))
    print(part2_score(input_filename))


if __name__ == '__main__':
    main(sys.argv)

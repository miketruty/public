#!/usr/bin/python3
# Read the input, look for enclosed and overlapping ranges.

import os
import sys


def score_group1(pairs: str) -> int:
    """Return 1 if one fully contained by the other.

    I think I can do this with set subtraction.
    """
    e1, e2 = pairs.split(',')
    e1_ss = e1.split('-')  ## ss = startstop
    e2_ss = e2.split('-')  ## ss = startstop
    e1_set = set(range(int(e1_ss[0]), int(e1_ss[1]) + 1))
    e2_set = set(range(int(e2_ss[0]), int(e2_ss[1]) + 1))
    if e1_set - e2_set == set():
        return 1
    if e2_set - e1_set == set():
        return 1
    return 0


def part1_score(input_filename: str) -> int:
    """Check if 1 range fully enclosed by another.
    """
    score = 0
    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            score += score_group1(line.strip())

    return score


def score_group2(pairs: str) -> int:
    """Return 1 if one fully contained by the other.

    I think I can do this with set subtraction.
    """
    e1, e2 = pairs.split(',')
    e1_ss = e1.split('-')  ## ss = startstop
    e2_ss = e2.split('-')  ## ss = startstop
    e1_set = set(range(int(e1_ss[0]), int(e1_ss[1]) + 1))
    e2_set = set(range(int(e2_ss[0]), int(e2_ss[1]) + 1))
    if len(e1_set & e2_set) > 0:
        return 1
    return 0


def part2_score(input_filename: str) -> int:
    """Check if 1 range overlaps at all with the other
    """
    score = 0
    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            score += score_group2(line.strip())

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

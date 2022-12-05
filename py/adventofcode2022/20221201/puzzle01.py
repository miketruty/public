#!/usr/bin/python3
# Read the input and determine the largest elf-calorie sum.

import heapq
import os
import sys


def part1_top_elf(input_filename: str) -> int:
    """Find the large sum input group and return the sum.
    """
    highest_sum = 0
    with open(input_filename, 'rt') as input_file:
        current_sum = 0
        for line in input_file:
            line = line.strip()
            if not line:
                if current_sum > highest_sum:
                    highest_sum = current_sum
                current_sum = 0
                continue
            current_sum += int(line)

    return highest_sum


def part2_top3_elves(input_filename: str) -> int:
    """Find the top 3 large sum input groups and return the sum.
    """
    maxheap = []

    with open(input_filename, 'rt') as input_file:
        current_sum = 0
        for line in input_file:
            line = line.strip()
            if not line:
                if current_sum:
                    heapq.heappush(maxheap, current_sum)
                current_sum = 0
                continue
            # by default heapq makes minheap - negate for maxheap
            current_sum -= int(line)

    # Now, sum the highest 3
    highest_sum = (heapq.heappop(maxheap) + heapq.heappop(maxheap) +
                   heapq.heappop(maxheap))

    return highest_sum * -1  # invert value for maxheap


def main(argv):
    input_filename = argv[1] if len(argv) > 1 else 'input'
    if not os.path.isfile(input_filename):
        print(f'Error: cannot find file {input_filename}')
        sys.exit(-1)
    print(part1_top_elf(input_filename))
    print(part2_top3_elves(input_filename))


if __name__ == '__main__':
    main(sys.argv)

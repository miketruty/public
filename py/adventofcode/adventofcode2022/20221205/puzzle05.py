#!/usr/bin/python3
# Set up the stacks, then do the moves, and read the stack tops.

from collections import deque
import os
import sys


def do_init_stacks(d: list, line: str) -> None:
    if not d:
        # init stack data
        stack_count = (len(line) + 1) // 4
        for _ in range(stack_count):
            d.append(deque())
    for i in range(1, len(line), 4):
        if line[i] == ' ':
            continue
        stack_num = (i - 1) // 4
        # If I appendleft() here, I can treat the stack with
        # append/pop (right) for the moves.
        d[stack_num].appendleft(line[i])


def do_move1(d: list, line: str) -> None:
    move_tokens = line.split()
    move_count = int(move_tokens[1])
    move_from = int(move_tokens[3]) - 1
    move_to = int(move_tokens[5]) - 1
    for _ in range(move_count):
        d[move_to].append(d[move_from].pop())


def part1_score(input_filename: str) -> str:
    """Load the stacks, rearrange, print stack tops.
    """
    d = []  # list of stacks
    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            if line.strip().startswith('['):
                do_init_stacks(d, line)
            elif line.startswith('move'):
                do_move1(d, line)

    result = []
    for s in d:
        if len(s) > 0:
            result.append(s.pop())
    return ''.join(result)


def do_move2(d: list, line: str) -> None:
    """New move, need a temp stack to handle order of multi-item.
    """
    move_tokens = line.split()
    move_count = int(move_tokens[1])
    move_from = int(move_tokens[3]) - 1
    move_to = int(move_tokens[5]) - 1

    temp_stack = deque()

    for _ in range(move_count):
        temp_stack.append(d[move_from].pop())

    for _ in range(move_count):
        d[move_to].append(temp_stack.pop())


def part2_score(input_filename: str) -> str:
    """Load the stacks, rearrange, print stack tops.
    """
    d = []  # list of stacks
    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            if line.strip().startswith('['):
                do_init_stacks(d, line)
            elif line.startswith('move'):
                do_move2(d, line)

    result = []
    for s in d:
        if len(s) > 0:
            result.append(s.pop())
    return ''.join(result)


def main(argv):
    input_filename = argv[1] if len(argv) > 1 else 'input'
    if not os.path.isfile(input_filename):
        print(f'Error: cannot find file {input_filename}')
        sys.exit(-1)
    print(part1_score(input_filename))
    print(part2_score(input_filename))


if __name__ == '__main__':
    main(sys.argv)

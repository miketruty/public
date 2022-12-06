#!/usr/bin/python3
# Look through a oneline message for the first unique sequence.

from collections import deque
import os
import sys


def part_score(input_filename: str, token_len) -> str:
    """Use a deque as a queue with a max-length
    """
    d = deque([], token_len)  # queue with max length token_len
    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            for i in range(len(line)):
                d.append(line[i])
                if len(d) == token_len and len(set(d)) == token_len:
                    return i + 1
    return 0


def main(argv):
    input_filename = argv[1] if len(argv) > 1 else 'input'
    if not os.path.isfile(input_filename):
        print(f'Error: cannot find file {input_filename}')
        sys.exit(-1)
    print(part_score(input_filename, 4))
    print(part_score(input_filename, 14))


if __name__ == '__main__':
    main(sys.argv)

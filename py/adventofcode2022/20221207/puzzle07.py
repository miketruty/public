#!/usr/bin/python3
# Process a sequence of commands to build a dir-tree with file/dir sizes.
#
# This feels a little messy. The line parsing isn't especially robust, and
# it feels like using a dict/deque might not be the most efficient
# representation for a tree.

from collections import deque
import os
import sys


def add_dir(d: dict, curdir: deque, newdir: str) -> None:
    while len(curdir) > 0:
        d = d[curdir.popleft()]
    d[newdir] = {'.': 0}


def add_file(d: dict, curdir: deque, fsize: int, fname: str) -> None:
    d['.'] += fsize
    while len(curdir) > 0:
        d = d[curdir.popleft()]
        d['.'] += fsize
    d[fname] = fsize


def sum_big_dirs(d: dict) -> int:
    """Sum all dirs <= 100000.

    Traverse through all dicts in the dict iteratively with a queue.
    """
    cur_sum = 0
    todo = deque([d])
    while len(todo) > 0:
        current_d = todo.pop()
        for e in current_d:
            if e == '.':
                if current_d[e] <= 100000:
                    cur_sum += current_d[e]
            elif isinstance(current_d[e], dict):
                todo.appendleft(current_d[e])

    return cur_sum


def find_smallest_del_dir(d: dict) -> int:
    """find smallest dir big enough to delete.

    Traverse through all dicts in the dict iteratively with a queue.
    """
    smallest = d['.']
    free = 70000000 - smallest
    need = 30000000 - free

    todo = deque([d])
    while len(todo) > 0:
        current_d = todo.pop()
        for e in current_d:
            if e == '.':
                if current_d[e] < smallest and current_d[e] > need:
                    smallest = current_d[e]
            elif isinstance(current_d[e], dict):
                todo.appendleft(current_d[e])

    return smallest


def part1_setup(input_filename: str) -> dict:
    """I think a dict for the dir and a deque for current dir.
    """
    d = {'.': 0}
    curdir = deque()

    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            line = line.strip()
            # print(f'doing line: {line}')
            if line == '$ cd /':
                curdir.clear()
            elif line == '$ cd ..':
                curdir.pop()
            elif line.startswith('$ cd'):
                dir = line.split()[2]
                curdir.append(dir)
            elif line == 'ls':
                continue
            elif line.startswith('dir'):
                newdir = line.split()[1]
                add_dir(d, curdir.copy(), newdir)
            elif line[0].isdigit():
                parts = line.split()
                fsize = int(parts[0])
                fname = parts[1]
                add_file(d, curdir.copy(), fsize, fname)

    return d


def main(argv):
    input_filename = argv[1] if len(argv) > 1 else 'input'
    if not os.path.isfile(input_filename):
        print(f'Error: cannot find file {input_filename}')
        sys.exit(-1)
    d = part1_setup(input_filename)
    print(f'root of d is {d["."]} big.')
    print(sum_big_dirs(d))
    print(find_smallest_del_dir(d))


if __name__ == '__main__':
    main(sys.argv)

#!/usr/bin/python3
# Set up the stacks, then do the moves, and read the stack tops.

import os
import sys


class Forest(object):

    def __init__(self):
        self.size = 0
        self.trees = []  # List of lists (rows).
        self.vcount = 0
        self.visible = []

    def _init_visible(self):
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if (i == 0 or i == self.size - 1 or
                    j == 0 or j == self.size - 1):
                    row.append(1)
                    self.vcount += 1
                else:
                    row.append(0)
            self.visible.append(row)

    def add_row(self, line: str):
        if self.size == 0:
            if len(line) > 0:
                self.size = len(line)
                self._init_visible()
        else:
            if len(line) != self.size:
                print('Error: input is not square.')
                sys.exit(-1)

        self.trees.append([int(c) for c in line])

    def __str__(self):
        result = ''
        for row in self.trees:
            result += ' '.join([str(c) for c in row]) + '\n'
        return result

    def _look_blocked_left(self, i: int, j: int):
        if self.visible[i][j]:
            return
        col = j
        while col > 0:
            if self.trees[i][j] <= self.trees[i][col - 1]:
                break
            col -= 1
        if col == 0:
            self.visible[i][j] = 1
            self.vcount += 1

    def _look_blocked_up(self, i: int, j: int):
        if self.visible[i][j]:
            return
        row = i
        while row > 0:
            if self.trees[i][j] <= self.trees[row - 1][j]:
                break
            row -= 1
        if row == 0:
            self.visible[i][j] = 1
            self.vcount += 1

    def _look_blocked_right(self, i: int, j: int):
        if self.visible[i][j]:
            return
        col = j
        while col < self.size - 1:
            if self.trees[i][j] <= self.trees[i][col + 1]:
                break
            col += 1
        if col == self.size - 1:
            self.visible[i][j] = 1
            self.vcount += 1

    def _look_blocked_down(self, i: int, j: int):
        if self.visible[i][j]:
            return
        row = i
        while row < self.size - 1:
            if self.trees[i][j] <= self.trees[row + 1][j]:
                break
            row += 1
        if row == self.size - 1:
            self.visible[i][j] = 1
            self.vcount += 1

    def _look_visible_left(self, i: int, j: int):
        col = j - 1
        found = 0
        while col >= 0:
            found += 1
            if self.trees[i][j] <= self.trees[i][col]:
                break
            col -= 1
        return found

    def _look_visible_up(self, i: int, j: int):
        row = i - 1
        found = 0
        while row >= 0:
            found += 1
            if self.trees[i][j] <= self.trees[row][j]:
                break
            row -= 1
        return found

    def _look_visible_right(self, i: int, j: int):
        col = j + 1
        found = 0
        while col < self.size:
            found += 1
            if self.trees[i][j] <= self.trees[i][col]:
                break
            col += 1
        return found

    def _look_visible_down(self, i: int, j: int):
        row = i + 1
        found = 0
        while row < self.size:
            found += 1
            if self.trees[i][j] <= self.trees[row][j]:
                break
            row += 1
        return found

    def count_visible_trees(self):
        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                self._look_blocked_left(i, j)
                self._look_blocked_up(i, j)
                self._look_blocked_right(i, j)
                self._look_blocked_down(i, j)
        return self.vcount

    def score_visible_trees(self):
        high_score = 1
        # edge trees score = 0, skip them
        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                score = 1
                score *= self._look_visible_left(i, j)
                score *= self._look_visible_up(i, j)
                score *= self._look_visible_right(i, j)
                score *= self._look_visible_down(i, j)
                if score > high_score:
                    high_score = score
        return high_score


def part1_score(input_filename: str) -> int:
    """Load up the forest (grid). Flag visible trees in the forest.
    """
    f = Forest()
    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            f.add_row(line.strip())
    return f.count_visible_trees()


def part2_score(input_filename: str) -> int:
    """Load up the forest (grid). Score visible trees in the forest.
    """
    f = Forest()
    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            f.add_row(line.strip())
    return f.score_visible_trees()


def main(argv):
    input_filename = argv[1] if len(argv) > 1 else 'input'
    if not os.path.isfile(input_filename):
        print(f'Error: cannot find file {input_filename}')
        sys.exit(-1)
    print(part1_score(input_filename))
    print(part2_score(input_filename))


if __name__ == '__main__':
    main(sys.argv)

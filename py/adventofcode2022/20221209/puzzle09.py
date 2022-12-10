#!/usr/bin/python3
# Model rope physics. Given path of head, simulate path of tail.
# I didn't model this with a grid at all. I just track everything with
# coordinate indices. Without a standard grid that means I have both positive
# and negative coordinates; I start at 0,0.

import os
import sys


ENABLE_PLOTS = False


class Coord(object):
    """Make it easier to reason about coordinate manipulation.
    """

    def __init__(self, label, x=0, y=0):
        self.label = str(label)
        self.x = x
        self.y = y

    def move_right(self):
        self.y += 1

    def move_left(self):
        self.y -= 1

    def move_up(self):
        self.x += 1

    def move_down(self):
        self.x -= 1

    def make_tuple(self):
        return (self.x, self.y)

    def __str__(self):
        return f'({self.x},{self.y})'

    def is_adjacent(self, c):
        return (abs(self.x - c.x) <= 1 and
                abs(self.y - c.y) <= 1)

    def is_same_row(self, c):
        return self.x == c.x

    def is_same_col(self, c):
        return self.y == c.y

    def follow_row(self, c):
        if c.y > self.y:
            self.y += 1
        else:
            self.y -= 1

    def follow_col(self, c):
        if c.x > self.x:
            self.x += 1
        else:
            self.x -= 1

    def follow_diag(self, c):
        self.follow_col(c)
        self.follow_row(c)


class RopeModel(object):

    def __init__(self, tail_count, size):
        self.tail_count = tail_count
        self.size = size  # number of coordinates
        self.head_coord = Coord(0)
        self.tail_coords = [Coord(i + 1) for i in range(self.tail_count)]
        self.head_locations = set()
        self.tail_locations = set()
        self.width = 3  # width of cell for printing

    def plot_model(self):
        if not ENABLE_PLOTS:
            return
        # Just center 0,0 in the middle and allow for -size:+size grid.
        stub = '.'

        coords = {}
        for c in [self.head_coord] + self.tail_coords:
            t = c.make_tuple()
            if t not in coords:
                coords[t] = c.label.center(self.width)

        if self.size % 2 == 0:
            self.size += 1  # Helps to get low/high right
        high = self.size // 2
        low = high * -1

        grid = []  # list of lists
        header = [''.center(self.width)]
        for i in range(low, high + 1):
            index = str(i).center(self.width)
            header.append(index)
            row = [index]
            for j in range(low, high + 1):
                row.append(coords.get((i, j), stub.center(self.width)))
            grid.append(row)

        # Print it
        print(' '.join(header))
        for row in grid:
            print(' '.join(row))
        print('-' * 40)

    def _get_tail_coord(self):
        return self.tail_coords[self.tail_count - 1]

    def _move_head(self, direction: str) -> None:
        """Move the head location 1 space."""
        if direction == 'R':
            self.head_coord.move_right()
        elif direction == 'L':
            self.head_coord.move_left()
        elif direction == 'U':
            self.head_coord.move_up()
        elif direction == 'D':
            self.head_coord.move_down()
        else:
            print('Error: unknown direction: {direction}')
            sys.exit(-1)
        self.head_locations.add(self.head_coord.make_tuple())

    def _move_tail(self) -> None:
        """Update the tail location based on head."""
        prev_coord = self.head_coord
        for c in self.tail_coords:
            if c.is_adjacent(prev_coord):
                break
            # If same row, follow
            if c.is_same_row(prev_coord):
                c.follow_row(prev_coord)
            elif c.is_same_col(prev_coord):
                c.follow_col(prev_coord)
            else:
                c.follow_diag(prev_coord)
            prev_coord = c

        self.tail_locations.add(self._get_tail_coord().make_tuple())

    def count_tail_locations(self):
        return len(self.tail_locations)

    def move_head_tail(self, line: str) -> None:
        """Parse/move head coordinate, then adjust tail.
        """
        direction, spaces_moved = line.split()
        for _ in range(int(spaces_moved)):
            if ENABLE_PLOTS:
                print(f'move {direction}')
            self._move_head(direction)
            self._move_tail()
            self.plot_model()


def part1_score(input_filename: str) -> int:
    """Set up a rope mode with head/tail coordinates and work lines as moves.
    """
    r = RopeModel(1, 30)
    r.plot_model()
    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            r.move_head_tail(line.strip())
    return r.count_tail_locations()


def part2_score(input_filename: str) -> int:
    """Load up the forest (grid). Score visible trees in the forest.
    """
    r = RopeModel(9, 40)
    r.plot_model()
    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            r.move_head_tail(line.strip())
    return r.count_tail_locations()


def main(argv):
    input_filename = argv[1] if len(argv) > 1 else 'input'
    if not os.path.isfile(input_filename):
        print(f'Error: cannot find file {input_filename}')
        sys.exit(-1)
    print('Part 1')
    print(part1_score(input_filename))
    print('Part 2')
    print(part2_score(input_filename))


if __name__ == '__main__':
    main(sys.argv)

#!/usr/bin/python3
# Model rope physics. Given path of head, simulate path of tail.
#
# In the example, a 6x5 grid is used and the tail visits 13 positions.
#
# Q: how do I decide how to size the grid?
# Q: where do I start/place HT to begin?
#
# Thought: do I need a grid at all? Can I just track the coordinates of the two
# and use relative comparisons to the two to model the movement without a 2-d
# grid? I'd love that.
#
# If I do that, it might be harder to visualize the current positions though.
# Maybe I don't care.

import os
import sys


class Coord(object):
    """Make it easier to reason about coordinate manipulation.
    """

    def __init__(self, x=0, y=0):
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

    def __init__(self):
        self.head_coord = Coord()
        self.tail_coord = Coord()
        self.head_locations = set()
        self.tail_locations = set()

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
        if not self.tail_coord.is_adjacent(self.head_coord):
            # If same row, follow
            if self.tail_coord.is_same_row(self.head_coord):
                self.tail_coord.follow_row(self.head_coord)
            elif self.tail_coord.is_same_col(self.head_coord):
                self.tail_coord.follow_col(self.head_coord)
            else:
                self.tail_coord.follow_diag(self.head_coord)

        self.tail_locations.add(self.tail_coord.make_tuple())

    def count_tail_locations(self):
        return len(self.tail_locations)

    def move_head_tail(self, line: str) -> None:
        """Parse/move head coordinate, then adjust tail.
        """
        direction, spaces_moved = line.split()
        for _ in range(int(spaces_moved)):
            self._move_head(direction)
            self._move_tail()


def part1_score(input_filename: str) -> int:
    """Load up the forest (grid). Flag visible trees in the forest.
    """
    r = RopeModel()
    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            r.move_head_tail(line.strip())
    return r.count_tail_locations()


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
    #print(part2_score(input_filename))


if __name__ == '__main__':
    main(sys.argv)

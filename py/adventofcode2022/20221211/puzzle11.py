#!/usr/bin/python3
# Model a CPU clock with 1 register X and 2 instructions:
# noop   - 1 cycle
# addx V - 2 cycles

from collections import deque
import os
import sys


class Monkey(object):

    def __init__(self, name):
        self._name = name
        self._items = deque()
        self._operation = ''  # new = old ...
        self._test_divisible = 1  # divisible by ...
        self._if_true_to = 0
        self._if_false_to = 0

        self._inspection_count = 0

    def get_name(self):
        return self._name

    def __str__(self):
        return (f'{self._name}\n' +
                f'  items: {self._items}\n' +
                f'  operation: {self._operation}\n' +
                f'  test divisible by: {self._test_divisible}\n' +
                f'  if true, throw to: {self._if_true_to}\n' +
                f'  if false, throw to: {self._if_false_to}\n')

    def extend_items(self, items):
        self._items.extend(items)

    def add_item(self, item):
        self._items.append(item)

    def get_item_count(self):
        return len(self._items)

    def pop_item(self):
        self._inspection_count += 1
        return self._items.popleft()  # queue - add right, pop left

    def add_operation(self, operation):
        self._operation = operation

    def get_operation(self):
        return self._operation

    def add_test_divisible(self, divisible_by):
        self._test_divisible = divisible_by

    def get_test_divisible(self):
        return self._test_divisible

    def add_if_true(self, throw_to):
        self._if_true_to = throw_to

    def get_if_true(self):
        return self._if_true_to

    def add_if_false(self, throw_to):
        self._if_false_to = throw_to

    def get_if_false(self):
        return self._if_false_to

    def get_inspection_count(self):
        return self._inspection_count


class Jungle(object):

    def __init__(self):
        self._monkeys = {}

    def add_monkey(self, m):
        self._monkeys[m.get_name()] = m

    def throw_item(self, to_m, item):
        self._monkeys[f'Monkey {to_m}'].add_item(item)

    def calc_monkey_business(self):
        counts = []
        for m in self._monkeys.values():
            counts.append(m.get_inspection_count())
            print(f'{m.get_name()} inspected items {m.get_inspection_count()} times')
        counts = sorted(counts)
        return counts[-1] * counts[-2]

    def do_round(self):
        """Run through each monkey once and update.
        """
        for i in range(len(self._monkeys)):
            m = self._monkeys[f'Monkey {i}']
            print(m.get_name())
            for _ in range(m.get_item_count()):
                item = m.pop_item()  # inspect item with worry level
                print(f'  Monkey inspects an item with a worry level of {item}')
                old = item
                new = eval(m.get_operation())
                print(f'    Worry level is multiplied to {new}')
                new //= 3  # relief that monkey inspection didn't damage
                print(f'    Monkey gets bored with item. Worry level to {new}')
                if new % m.get_test_divisible() != 0:
                    print(f'    Current worry level is not divisible by {m.get_test_divisible()}')
                    print(f'    Item with worry level {new} is thrown to monkey {m.get_if_false()}')
                    new_m = m.get_if_false()
                else:
                    print(f'    Current worry level is divisible by {m.get_test_divisible()}')
                    print(f'    Item with worry level {new} is thrown to monkey {m.get_if_true()}')
                    new_m = m.get_if_true()
                self.throw_item(new_m, new)
            print()


def part1_score(input_filename: str) -> int:
    """Set up a multi-monkey model.
    """
    j = Jungle()
    with open(input_filename, 'rt') as input_file:
        m = None
        for line in input_file:
            if line.startswith('Monkey'):
                m = Monkey(line.strip()[:-1])
            elif line.strip().startswith('Starting items:'):
                item_str = line.strip().split(':')[1].split(',')
                m.extend_items([int(i.strip()) for i in item_str])
            elif line.strip().startswith('Operation: new'):
                m.add_operation(line.strip().split(' new = ')[1])
            elif line.strip().startswith('Test: divisible by '):
                m.add_test_divisible(
                    int(line.strip().split('divisible by ')[1]))
            elif line.strip().startswith('If true:'):
                m.add_if_true(int(line.strip().split()[-1]))
            elif line.strip().startswith('If false:'):
                m.add_if_false(int(line.strip().split()[-1]))
            elif line.strip() == '':
                j.add_monkey(m)
        if m:
            j.add_monkey(m)
    for i in range(20):  # do 20 rounds
        j.do_round()
    return j.calc_monkey_business()


# def part2_score(input_filename: str):
#     """Set up CPU model with clock and track related sprite.
#     """
#     with open(input_filename, 'rt') as input_file:
#         instructions = deque([line.strip() for line in input_file])
#     cpu = CPUModel()
#     cpu.do_work(instructions)

def main(argv):
    input_filename = argv[1] if len(argv) > 1 else 'input'
    if not os.path.isfile(input_filename):
        print(f'Error: cannot find file {input_filename}')
        sys.exit(-1)
    print('Part 1')
    print(part1_score(input_filename))


if __name__ == '__main__':
    main(sys.argv)

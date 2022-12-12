#!/usr/bin/python3
# Model a CPU clock with 1 register X and 2 instructions:
# noop   - 1 cycle
# addx V - 2 cycles

from collections import deque
import os
import sys


class CPUModel(object):

    def __init__(self):
        self._clock = 1
        self._regX = 1
        self._icache = deque()

        self._signal_strength = 0  # cycle=20, 60, 100, 140, 180, 220, ...

        self._sprite = []
        self._buffer = []  # rendering

        self._update_sprite()  # based on regX = 1

    def get_signal_strength(self):
        return self._signal_strength

    def _update_ss(self):
        # Only if clock in 20, 60, 100, 140, 180, 220, ...
        if (self._clock - 20) % 40 == 0:
            # debug:
            # print(f'cycle: {self._clock}, regX: {self._regX} = '
            #       f'{self._clock * self._regX}')
            self._signal_strength += (self._clock * self._regX)

    def _is_work_remaining(self):
        return len(self._icache) > 0

    def _do_fetch(self, instructions: deque):
        i = instructions.popleft()
        if i == 'noop':
            self._icache.append(i)
        else:  # addx
            self._icache.append('noop')
            self._icache.append(i)

    def _do_cpu_tick(self):
        if self._is_work_remaining():
            i = self._icache.popleft()
            if i == 'noop':
                return
            v = int(i.split()[1])
            self._regX += v  # addx

    def _update_sprite(self):
        self._sprite = []
        if self._regX - 1 >= 0 and self._regX - 1 < 40:
            self._sprite.append(self._regX - 1)
        if self._regX >= 0 and self._regX < 40:
            self._sprite.append(self._regX)
        if self._regX + 1 >= 0 and self._regX + 1 < 40:
            self._sprite.append(self._regX + 1)

    def _do_render_tick(self):
        if len(self._buffer) in self._sprite:
            self._buffer.append('#')
        else:
            self._buffer.append('.')

        if len(self._buffer) >= 40:
            print(''.join(self._buffer))
            self._buffer = []
        return

    def do_work(self, instructions:deque) -> None:
        while instructions or self._is_work_remaining():
            if instructions:
                self._do_fetch(instructions)
            self._clock += 1  # order, based on example, seems arbitrary
            self._update_sprite()
            self._do_render_tick()
            self._do_cpu_tick()
            self._update_ss()


def part1_score(input_filename: str) -> int:
    """Set up a CPU model with a clock.
    """
    with open(input_filename, 'rt') as input_file:
        instructions = deque([line.strip() for line in input_file])
    cpu = CPUModel()
    cpu.do_work(instructions)
    return cpu.get_signal_strength()


def part2_score(input_filename: str):
    """Set up CPU model with clock and track related sprite.
    """
    with open(input_filename, 'rt') as input_file:
        instructions = deque([line.strip() for line in input_file])
    cpu = CPUModel()
    cpu.do_work(instructions)

def main(argv):
    input_filename = argv[1] if len(argv) > 1 else 'input'
    if not os.path.isfile(input_filename):
        print(f'Error: cannot find file {input_filename}')
        sys.exit(-1)
    print('Part 1')
    print(part1_score(input_filename))
    print('Part 2')
    part2_score(input_filename)


if __name__ == '__main__':
    main(sys.argv)

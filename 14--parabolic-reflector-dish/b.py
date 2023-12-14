#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys
import itertools
import time
import os
from collections import namedtuple


def main():
    grid = open(sys.argv[1]).read().splitlines()

    transposed = transpose(grid)
    time_machine = TimeMachine()

    for n in itertools.count(start=1):

        # Apply one spin cycle
        tilt_grid_west(transposed)
        transposed = rotccw(transposed)
        tilt_grid_west(transposed)
        transposed = rotccw(transposed)
        tilt_grid_west(transposed)
        transposed = rotccw(transposed)
        tilt_grid_west(transposed)
        transposed = rotccw(transposed)

        time_machine.append(n, total_load(transposed), str(transposed))

        if time_machine.period is not None:
            break

    answer = time_machine.predict(1000000000)
    print(answer)


def total_load(transposed):
    return sum(
        i
        for row in transposed
        for i, ch in enumerate(reversed(row), start=1)
        if ch == 'O'
    )


def tilt_grid_west(grid):
    for i, row in enumerate(grid):
        grid[i] = '#'.join(
            tilt_row_west(each)
            for each in row.split('#')
        )


def tilt_row_west(s):
    return ''.join(sorted(s, reverse=True))


def transpose(m):
    return [''.join(i) for i in zip(*m)]


def rotccw(original):
    return rotmat(rotmat(rotmat(original)))


def rotmat(original):
    return list(''.join(tpl) for tpl in zip(*original[::-1]))


LogEntry = namedtuple('LogEntry', 'x y signature')

class TimeMachine:
    '''
    Given an "eventually-periodic" function y = f(x), TimeMachine computes
    f(SOME_LARGE_X).
    '''

    def __init__(self):
        self.log = {}
        self.by_signature = {}
        self.period = None

    def append(self, x, y, signature):
        entry = LogEntry(x, y, signature)
        self.log[x] = entry
        if signature in self.by_signature:
            previous_entry = self.by_signature[signature]
            self.period = x - previous_entry.x
        else:
            self.by_signature[signature] = entry

    def predict(self, x):
        assert self.period is not None

        by_remainder = {}

        last_idx = max(self.log)
        for old_x in range(last_idx - self.period + 1, last_idx + 1):
            by_remainder[old_x % self.period] = self.log[old_x].y

        return by_remainder[x % self.period]


if __name__ == '__main__':
    main()

#!./numpy_env/bin/python3
'''
Alternate solution using numpy.

Install:
    python3 -m venv numpy_env
    . numpy_env/bin/activate
    pip install -r numpy_requirements.txt

Usage:
    Must have installed numpy first (see above)
    ./b.numpy.py PATH_TO_INPUT_FILE
'''

import sys
from collections import namedtuple
import itertools

import numpy as np


def main():
    grid = np.array([list(line) for line in open(sys.argv[1]).read().splitlines()])

    time_machine = TimeMachine()
    for n in itertools.count(start=1):
        # Apply one spin cycle
        tilt_north(grid)
        tilt_west(grid)
        tilt_south(grid)
        tilt_east(grid)

        time_machine.append(n, total_load(grid), to_full_string(grid))

        if time_machine.period is not None:
            break

    answer = time_machine.predict(1000000000)
    print(answer)


def total_load(grid):
    HEIGHT, WIDTH = grid.shape
    return sum(
        i
        for c in range(WIDTH)
        for i, ch in enumerate(grid[::-1,c], start=1)
        if ch == 'O'
    )


def tilt_north(grid):
    HEIGHT, WIDTH = grid.shape
    for c in range(WIDTH):
        grid[::,c] = tilt_vector(grid[::,c], 'start')


def tilt_south(grid):
    HEIGHT, WIDTH = grid.shape
    for c in range(WIDTH):
        grid[::,c] = tilt_vector(grid[::,c], 'end')


def tilt_west(grid):
    HEIGHT, WIDTH = grid.shape
    for r in range(HEIGHT):
        grid[r] = tilt_vector(grid[r], 'start')


def tilt_east(grid):
    HEIGHT, WIDTH = grid.shape
    for r in range(HEIGHT):
        grid[r] = tilt_vector(grid[r], 'end')


def tilt_vector(v, towards_direction):
    s = ''.join(v)
    chunks = s.split('#')
    tilted = [tilt_chunk(each, towards_direction) for each in chunks]
    result = [*'#'.join(tilted)]
    return result


def tilt_chunk(chunk, towards_direction):
    assert towards_direction in ['start', 'end']
    reverse = towards_direction == 'start'
    return ''.join(sorted(chunk, reverse=reverse))


def to_full_string(numpy_array):
    with np.printoptions(threshold=np.inf):
        return str(numpy_array)


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

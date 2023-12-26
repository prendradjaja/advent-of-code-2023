#!/usr/bin/env python3
'''
Usage for puzzle input:
    ./a.py INPUT_FILE -p

Usage for example input:
    ./a.py INPUT_FILE -e

-p or -e must be provided so we know whether the Elf needs 6 more steps today
or 64.
'''

import sys


DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def main():
    # Parse args
    if len(sys.argv) < 3 or not sys.argv[2] in ['-p', '-e']:
        print(__doc__.strip())
        exit()
    path = sys.argv[1]
    step_count = {'-p': 64, '-e': 6}[sys.argv[2]]

    # Read input file
    world = open(path).read().splitlines()

    # Find start position
    for pos, ch in enumerate2d(world):
        if ch == 'S':
            start = pos
            break

    # Simulate
    reachable = {pos}
    for _ in range(step_count):
        reachable = iterate(world, reachable)

    answer = len(reachable)
    print(answer)


def iterate(world, reachable):
    def neighbors(pos):
        for offset in DIRECTIONS:
            pos2 = addvec(pos, offset)
            if in_bounds(world, pos2) and getitem(world, pos2) != '#':
                yield pos2

    return {
        pos2
        for pos in reachable
        for pos2 in neighbors(pos)
    }


def getitem(grid, pos):
    assert in_bounds(grid, pos)
    r, c = pos
    return grid[r][c]


def in_bounds(grid, pos):
    r, c = pos
    return (
        0 <= r < len(grid) and
        0 <= c < len(grid[0])
    )


def enumerate2d(grid):
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            yield (r, c), value


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


if __name__ == '__main__':
    main()

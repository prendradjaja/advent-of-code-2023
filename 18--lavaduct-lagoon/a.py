#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
'''

import sys


DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}


def main():
    pos = (0, 0)
    cleared = {pos}
    for line in open(sys.argv[1]).read().splitlines():
        direction, n, color = line.split()
        n = int(n)
        for _ in range(n):
            pos = addvec(pos, DIRECTIONS[direction])
            cleared.add(pos)

    rmin = min(r for r, c in cleared)
    rmax = max(r for r, c in cleared)
    cmin = min(c for r, c in cleared)
    cmax = max(c for r, c in cleared)

    # Pick a point on the interior. Any will do; we'll pick one next to the
    # bottom edge.
    interior_point = [
        (r - 1, c)
        for r, c in cleared
        if r == rmax
        and (r - 1, c) not in cleared
    ][0]

    sys.setrecursionlimit(100_000)
    flood_fill(cleared, interior_point)

    print(len(cleared))


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


def flood_fill(cleared, pos):
    neighbors = [addvec(pos, offset) for offset in DIRECTIONS.values()]
    for each in neighbors:
        if each not in cleared:
            cleared.add(each)
            flood_fill(cleared, each)


if __name__ == '__main__':
    main()

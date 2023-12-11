#!/usr/bin/env python3
'''
Usage:
    ./b.py PATH_TO_INPUT_FILE EXPANSION_FACTOR
Example:
    ./b.py ex 100

Don't forget to change the 100 to 1000000 when running against the puzzle
input! (For readability, 1_000_000 is also allowed.)
'''

import itertools
import sys


def main():
    if len(sys.argv) < 3:
        print(__doc__.strip())
        exit()

    image = open(sys.argv[1]).read().splitlines()
    expansion_factor = int(sys.argv[2])
    galaxies = [
        pos for pos, ch in enumerate2d(image)
        if ch == '#'
    ]

    # Find empty rows and cols:
    #     I did this step differently in b.py vs a.py. Didn't need to, but I
    # thought it'd be nice to make a new implementation that matches the new
    # data representation.
    empty_rows = [
        r for r in range(len(image))
        if not any(pos[0] == r for pos in galaxies)
    ]
    empty_cols = [
        c for c in range(len(image[0]))
        if not any(pos[1] == c for pos in galaxies)
    ]

    # Expand rows and cols
    for r in reversed(empty_rows):
        for i, pos in enumerate(galaxies):
            gr, gc = pos
            if gr > r:
                galaxies[i] = (gr + (expansion_factor - 1), gc)
    for c in reversed(empty_cols):
        for i, pos in enumerate(galaxies):
            gr, gc = pos
            if gc > c:
                galaxies[i] = (gr, gc + (expansion_factor - 1))

    # Measure distances
    answer = sum(
        manhattan_distance(g, h)
        for g, h in itertools.combinations(galaxies, 2)
    )
    print(answer)


def enumerate2d(grid):
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            yield (r, c), value


def manhattan_distance(pos1, pos2):
    dr, dc = tuple(p - q for p, q in zip(pos1, pos2))
    return abs(dr) + abs(dc)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
'''

import itertools
import sys


def main():
    image = [list(line) for line in open(sys.argv[1]).read().splitlines()]

    # Find empty rows and cols
    empty_rows = [
        r for r in range(len(image))
        if set(image[r]) == {'.'}
    ]
    empty_cols = [
        c for c in range(len(image[0]))
        if all(image[r][c] == '.' for r in range(len(image)))
    ]

    # Expand rows and cols
    for r in reversed(empty_rows):
        image.insert(r, ['.'] * len(image[0]))

    transposed = transpose(image)
    for c in reversed(empty_cols):
        transposed.insert(c, ['.'] * len(transposed[0]))
    image = transpose(transposed)

    # Measure distances
    galaxies = [
        pos for pos, ch in enumerate2d(image)
        if ch == '#'
    ]
    answer = sum(
        manhattan_distance(g, h)
        for g, h in itertools.combinations(galaxies, 2)
    )
    print(answer)


def transpose(m):
    """
    >>> transpose([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]
    """
    return [list(i) for i in zip(*m)]


def enumerate2d(grid):
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            yield (r, c), value


def manhattan_distance(pos1, pos2):
    dr, dc = tuple(p - q for p, q in zip(pos1, pos2))
    return abs(dr) + abs(dc)


if __name__ == '__main__':
    main()

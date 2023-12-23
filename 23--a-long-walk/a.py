#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys


DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]

SLOPE_DIRECTIONS = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}


def main():
    world = open(sys.argv[1]).read().splitlines()

    (start_col,) = [
        c for c in range(len(world[0]))
        if world[0][c] == '.'
    ]
    start = (0, start_col)

    sys.setrecursionlimit(10_000)
    answer = get_longest_hike_length(world, (start,)) - 1
    print(answer)


def get_longest_hike_length(world, partial_hike):
    neighbors = get_neighbors(world, partial_hike)
    if not neighbors:
        return len(partial_hike)

    return max(
        get_longest_hike_length(world, partial_hike + (each,))
        for each in neighbors
    )


def get_neighbors(world, partial_hike):
    pos = partial_hike[-1]
    ch = getitem(world, pos)
    result = []
    for d in DIRECTIONS:
        pos2 = addvec(pos, d)
        if (
            ch in SLOPE_DIRECTIONS
            and d != SLOPE_DIRECTIONS[ch]
        ):
            # If direction is illegal, skip.
            # Else, direction is legal.
            continue

        if (
            in_bounds(world, pos2)
            and getitem(world, pos2) != '#'
            and pos2 not in partial_hike
        ):
            result.append(pos2)
    return result


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


def getitem(grid, pos):
    assert in_bounds(grid, pos)
    r, c = pos
    return grid[r][c]


def setitem(grid, pos, value):
    assert in_bounds(grid, pos)
    r, c = pos
    grid[r][c] = value


def in_bounds(grid, pos):
    r, c = pos
    return (
        0 <= r < len(grid) and
        0 <= c < len(grid[0])
    )


if __name__ == '__main__':
    main()

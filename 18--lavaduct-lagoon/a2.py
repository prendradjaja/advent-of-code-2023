#!/usr/bin/env python3.12
'''
Usage:
    ./a2.py PATH_TO_INPUT_FILE
'''

import sys
import itertools


DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}


def main():
    pos = (0, 0)
    vertices = []
    for line in open(sys.argv[1]).read().splitlines():
        direction, n, color = line.split()
        n = int(n)
        for _ in range(n):
            pos = addvec(pos, DIRECTIONS[direction])
        vertices.append(pos)

    # This approach is from _Kuroni_ on Reddit: https://old.reddit.com/r/adventofcode/comments/18evyu9/2023_day_10_solutions/kcqmhwk/
    answer = perimeter_rectilinear(vertices) + count_interior_points(vertices)
    print(answer)


def perimeter_rectilinear(polygon):
    '''
    Polygon must be rectilinear.
    '''
    total = 0
    for v, w in itertools.pairwise(polygon + [polygon[0]]):
        total += abs(sum(subvec(w, v)))
    return total


def count_interior_points(polygon):
    '''
    Polygon must be rectilinear and have only integer vertices.

    Uses Pick's Theroem:
    https://en.wikipedia.org/wiki/Pick%27s_theorem
    '''
    perimeter = perimeter_rectilinear(polygon)
    assert perimeter % 2 == 0
    half_perimeter = perimeter // 2

    my_area = area(polygon)
    assert int(my_area) == my_area
    my_area = int(my_area)

    return my_area + 1 - half_perimeter


def area(polygon):
    '''
    Shoelace formula
    https://en.wikipedia.org/wiki/Shoelace_formula
    '''
    total = 0
    for v, w in itertools.pairwise(polygon + [polygon[0]]):
        vr, vc = v
        wr, wc = w
        total += vr * wc
        total -= wr * vc
    return abs(total / 2)


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


def subvec(v, w):
    return tuple(a - b for a, b in zip(v, w))


if __name__ == '__main__':
    main()

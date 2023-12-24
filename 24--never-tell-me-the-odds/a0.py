#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys
from collections import namedtuple
import ast
import itertools
import math
from dataclasses import dataclass


Hailstone = namedtuple('Hailstone', 'pos vel')


def main():
    test_area_min = int(sys.argv[2])
    test_area_max = int(sys.argv[3])

    hailstones = []
    for line in open(sys.argv[1]).read().splitlines():
        pos, vel = line.split('@')
        pos = ast.literal_eval(pos.strip())
        vel = ast.literal_eval(vel.strip())

        # Disregard Z axis
        pos = pos[:2]
        vel = vel[:2]

        assert 0 not in vel

        hailstones.append(Hailstone(pos, vel))

    n = len(hailstones)
    hailstones2 = [
        each._replace(pos = addvec(each.pos, each.vel))
        for each in hailstones
    ]

    paths = []
    for h, h2 in zip(hailstones, hailstones2):
        paths.append(LinearEquation.from_points(h.pos, h2.pos))

    answer = 0
    for i, j in itertools.combinations(range(n), 2):
        path1 = paths[i]
        path2 = paths[j]
        if path1.count_intersections(path2) != 1:
            continue
        intersection = path1.find_intersection(path2)
        if not is_forwards(hailstones[i], intersection):
            continue
        if not is_forwards(hailstones[j], intersection):
            continue
        if not (
            test_area_min <= intersection[0] <= test_area_max and
            test_area_min <= intersection[1] <= test_area_max
        ):
            continue
        answer += 1

    print(answer)


def is_forwards(hailstone, point):
    '''
    Return True if and only if POINT is in HAILSTONE's "forward quadrant".
    '''
    return signvec(subvec(point, hailstone.pos)) == signvec(hailstone.vel)


@dataclass
class LinearEquation:
    m: ...  # slope
    b: ...  # y-intercept

    def __call__(self, x):
        return self.m * x + self.b

    @classmethod
    def from_points(cls, p1, p2):
        '''
        >>> LinearEquation.from_points((1, 2), (3, 3))
        LinearEquation(m=0.5, b=1.5)
        '''
        x1, y1 = p1
        x2, y2 = p2
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        return LinearEquation(m, b)

    def count_intersections(self, other):
        '''
        Parallel lines do not cross
        >>> LinearEquation(1, 0).count_intersections(LinearEquation(1, 1))
        0

        ...except if they're the same line
        >>> LinearEquation(1, 0).count_intersections(LinearEquation(1, 0))
        inf

        Non-parallel lines do cross
        >>> LinearEquation(1, 0).count_intersections(LinearEquation(0, 0))
        1
        '''
        if not my_isclose(self.m, other.m):
            return 1
        elif my_isclose(self.b, other.b):
            return math.inf
        else:  # Slopes are equal but y-intercepts are different
            return 0

    def intersects(self, other):
        return bool(self.count_intersections(other))

    def find_intersection(self, other):
        '''
        >>> line1 = LinearEquation.from_points((1, 1), (3, 1))
        >>> line2 = LinearEquation.from_points((2, 0), (3, 1))
        >>> line1.find_intersection(line2)
        (3.0, 1.0)
        '''
        assert self.count_intersections(other) == 1
        x = (other.b - self.b) / (self.m - other.m)
        y = self(x)
        return x, y


def my_isclose(a, b):
    epsilon = 1e-05
    return abs(a - b) < epsilon


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


def subvec(v, w):
    return tuple(a - b for a, b in zip(v, w))


def absvec(v):
    return tuple(abs(a) for a in v)


def signvec(v):
    return tuple(sign(a) for a in v)


def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0


def manhattan_distance(v, w):
    return sum(absvec(subvec(v, w)))


if __name__ == '__main__':
    main()

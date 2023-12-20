#!/usr/bin/env python3.12
'''
This is a standalone module implementing the math used in this problem
(usable also for Day 10). b.py could import this, but it doesn't, so it can
stand on its own too.

Given a rectilinear polygon with integer vertices specified by its vertices,
we can find:

(Rectilinear: 1: All angles are right angles and 2: all edges are either
horizontal or vertical. In some uses, rectilinear only means #1, but here we
require both.)

- Area: Use Shoelace Formula
- Number of integer points on the boundary of the polygon:
    - For a rectilinear polygon with integer vertices, this is just the
      perimeter
- Number of integer points in the interior of the polygon: Pick's Theorem

Actually, some of these are more widely applicable:

- Shoelace Formula works for any simple polygon.
- Pick's Theorem works for any simple polygon with integer vertices.

(Simple polygon: No self-intersections, no holes)

But my test cases and use cases are rectilinear.
'''

import itertools


# A polygon is given as a list of vertices. They must be specified in order
# (clockwise or counterclockwise, doesn't matter) along the perimeter (i.e.
# they cannot be given in just an arbitrary order; that would specify a
# different polygon).
type Polygon = list[Vertex]

# A vertex is a pair of coordinates. Sign convention: (row, col), with down
# and right being positive respectively.
type Vertex = tuple[int, int]


DIRECTIONS = [
    UP := (-1, 0),
    DOWN := (1, 0),
    LEFT := (0, -1),
    RIGHT := (0, 1),
]


def main():
    SQUARE = [(0, 0), (3, 0), (3, 3), (0, 3)]
    RECTANGLE = [(0, 0), (-3, 0), (-3, -5), (0, -5)]
    # BLOB is the example from https://adventofcode.com/2023/day/18
    BLOB = [(0, 6), (5, 6), (5, 4), (7, 4), (7, 6), (9, 6), (9, 1), (7, 1), (7, 0), (5, 0), (5, 2), (2, 2), (2, 0), (0, 0)]

    assert area(SQUARE) == 9
    assert perimeter_rectilinear(SQUARE) == 12
    assert count_interior_points(SQUARE) == 4

    assert area(RECTANGLE) == 15
    assert perimeter_rectilinear(RECTANGLE) == 16
    assert count_interior_points(RECTANGLE) == 8

    assert area(BLOB) == 42
    assert perimeter_rectilinear(BLOB) == 38
    assert count_interior_points(BLOB) == 24
    # 38 + 24 == 62, the answer for the example

    for shape in [SQUARE, RECTANGLE, BLOB]:
        draw(shape)
        print('Area:', area(shape))
        print('Perimeter:', perimeter_rectilinear(shape))
        print('# of interior points:', count_interior_points(shape))
        print()


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


def perimeter_rectilinear(rectilinear_polygon):
    '''
    Polygon must be rectilinear.
    '''
    polygon = rectilinear_polygon
    assert is_rectilinear(polygon)

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
    assert is_rectilinear(polygon)
    assert is_integer_vertices(polygon)

    perimeter = perimeter_rectilinear(polygon)
    assert perimeter % 2 == 0
    half_perimeter = perimeter // 2

    my_area = area(polygon)
    assert int(my_area) == my_area
    my_area = int(my_area)

    return my_area + 1 - half_perimeter


def is_rectilinear(polygon):
    for v, w in itertools.pairwise(polygon + [polygon[0]]):
        direction = signvec(subvec(w, v))
        if direction not in DIRECTIONS:
            return False
    return True


def is_integer_vertices(polygon):
    return all(
        float(coordinate).is_integer()  # Works for both e.g. 6.0 and 6
        for vertex in polygon
        for coordinate in vertex
    )


def draw(rectilinear_polygon):
    polygon = rectilinear_polygon
    assert is_rectilinear(polygon)
    assert is_integer_vertices(polygon)

    boundary = set(polygon)
    for v, w in itertools.pairwise(polygon + [polygon[0]]):
        direction = signvec(subvec(w, v))
        while v != w:
            boundary.add(v)
            v = addvec(v, direction)

    rmin = min(r for r, c in polygon)
    rmax = max(r for r, c in polygon)
    cmin = min(c for r, c in polygon)
    cmax = max(c for r, c in polygon)
    for r in range(rmin, rmax + 1):
        for c in range(cmin, cmax + 1):
            if (r, c) in boundary:
                ch = '#'
            else:
                ch = '.'
            print(ch, end=' ')
        print()


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


def subvec(v, w):
    return tuple(a - b for a, b in zip(v, w))


def signvec(v):
    return tuple(sign(a) for a in v)


def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0


if __name__ == '__main__':
    main()

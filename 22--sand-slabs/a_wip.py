#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys
from dataclasses import dataclass
import collections
import ast


X, Y, Z = 0, 1, 2
DOWN = (0, 0, -1)


# TODO There are various todo-optim comments. First one to start with is
# definitely the collision map.


def main():
    '''
    >>> import unittest.mock
    >>> with unittest.mock.patch('sys.argv', [None, './ex']):
    ...    main()
    5
    '''
    bricks = []
    for line in open(sys.argv[1]).read().splitlines():
        start, end = line.split('~')
        start = ast.literal_eval(start)
        end = ast.literal_eval(end)
        bricks.append(Brick(start, end))

    # print([each.start[Z] for each in bricks])
    fall(bricks)

    answer = 0
    for brick in bricks:
        other_bricks = [b for b in bricks if b != brick]
        assert len(other_bricks) == len(bricks) - 1

        # n.b. It's ok to mutate other_bricks since (1) it's a copy and
        # (2) applying gravity to `other_bricks` with `fall()` doesn't affect
        # `bricks` because applying a gravity to one brick with
        # `Brick.fall1_copy()` doesn't modify the bricks.
        changed = fall(other_bricks)
        if not changed:
            answer += 1

    print(answer)


def fall(bricks):
    def can_fall1(brick):
        brick2 = brick.fall1_copy()
        # todo-optim: Shouldn't need to loop through every brick to find a
        # collision. Make and maintain a collision map.
        is_ground_collision = any(
            cube[Z] == 0
            for cube in brick2.cubes
        )
        is_any_collision = is_ground_collision or any(
            brick2.is_collision(other)
            for other in bricks
            if other != brick
        )
        return not is_any_collision

    changed = False
    while True:
        # todo-optim: Probably sorting bricks by elevation (What does that
        # mean? Not obvious) before looping through them would help.
        changed_inner = False
        for i, brick in enumerate(bricks):
            if can_fall1(brick):
                # todo-optim: Shouldn't need to fall by one unit repeatedly:
                # Fall as many units as available.
                bricks[i] = brick.fall1_copy()
                changed_inner = True
                changed = True

        # print([each.start[Z] for each in bricks])
        if not changed_inner:
            return changed


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


def subvec(v, w):
    return tuple(a - b for a, b in zip(v, w))


def range3d(start, end):
    '''
    Unlike range(), range3d includes both endpoints

    >>> range3d((2, 2, 2), (2, 2, 2))
    [(2, 2, 2)]
    >>> range3d((0, 0, 10), (1, 0, 10))
    [(0, 0, 10), (1, 0, 10)]
    >>> range3d((0, 0, 1), (0, 0, 10))
    [(0, 0, 1), (0, 0, 2), (0, 0, 3), (0, 0, 4), (0, 0, 5), (0, 0, 6), (0, 0, 7), (0, 0, 8), (0, 0, 9), (0, 0, 10)]
    '''
    delta = signvec(subvec(end, start))
    result = [start]
    pos = start
    while pos != end:
        pos = addvec(pos, delta)
        result.append(pos)
    return result


def signvec(v):
    return tuple(sign(a) for a in v)


def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0


@dataclass
class Brick:
    start: ...
    end: ...

    def __post_init__(self):
        self.cubes = set(range3d(self.start, self.end))

    def is_collision(self, other):
        return bool(self.cubes & other.cubes)

    def fall1_copy(self):
        '''
        Fall 1 unit down. This is a copying method, not a mutating method.
        '''
        return Brick(
            addvec(self.start, DOWN),
            addvec(self.end, DOWN)
        )


def show(bricks, ltr_axis):
    assert ltr_axis in [0, 1]

    # Names:
    # - A (or a) is the ltr_axis
    # - B (or b) is the other axis (neither A nor Z, but the other one)

    A = ltr_axis
    B = int(not A)

    foo = {
        (cube[A], cube[Z])
        for brick in bricks
        for cube in brick.cubes
    }

    for z in range(9, -1, -1):
        for a in range(3):
            if (a, z) in foo:
                ch = '#'
            else:
                ch = '.'
            print(ch, end='')
        print('', z)
    print()


if __name__ == '__main__':
    main()

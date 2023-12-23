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


def main():
    '''
    >>> import unittest.mock
    >>> with unittest.mock.patch('sys.argv', [None, './ex']):
    ...    main()
    5
    '''
    world = CollisionWorld()
    for line in open(sys.argv[1]).read().splitlines():
        start, end = line.split('~')
        start = ast.literal_eval(start)
        end = ast.literal_eval(end)
        world.add_brick(Brick(start, end))

    world.show(X, 0, 9)

    fall(world)

    world.show(X, 0, 9)

    # todo-optim
    answer = 0
    for i in range(len(world.bricks)):
        if i % 10 == 0:
            print('...', i)
        answer += get_chain_reaction_size(world, i)

    print(answer)


def get_chain_reaction_size(world, brick_idx):
    world2 = CollisionWorld()
    for i in range(len(world.bricks)):
        if i != brick_idx:
            world2.add_brick(world.bricks[i])

    # n.b. It's ok to mutate world2 since (1) it's a copy and (2) applying
    # gravity to `world2` with `fall()` doesn't affect `world` because
    # applying gravity to one brick with `Brick.fall1_copy()` doesn't modify
    # the bricks.
    changed = fall(world2)
    if not changed:
        return 0
    else:
        (bricks_changed,) = changed
        return len(bricks_changed)


def fall(world):
    def can_fall1(world, idx):
        brick = world.bricks[idx]
        brick2 = brick.fall1_copy()
        # todo-optim: Shouldn't need to loop through every brick to find a
        # collision. Make and maintain a collision map.
        is_ground_collision = any(
            cube[Z] == 0
            for cube in brick2.cubes
        )
        is_any_collision = is_ground_collision or world.is_collision(idx, brick2)
        return not is_any_collision

    changed = False
    bricks_changed = set()
    while True:
        # todo-optim: Probably sorting bricks by elevation (What does that
        # mean? Not obvious) before looping through them would help.
        changed_inner = False
        for i, brick in enumerate(world.bricks):
            if can_fall1(world, i):
                # todo-optim: Shouldn't need to fall by one unit repeatedly:
                # Fall as many units as available.
                world.replace_brick(i, brick.fall1_copy())
                bricks_changed.add(i)
                changed_inner = True
                changed = True

        # print([each.start[Z] for each in world.bricks])
        if not changed_inner:
            if not changed:
                return ()
            else:
                return (bricks_changed,)


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


class CollisionWorld:
    def __init__(self):
        self.bricks = []
        self.cubes = {}  # values are brick ids (indexes into self.bricks)

    def is_collision(self, idx, new_brick):
        for cube in new_brick.cubes:
            found_brick = self.cubes.get(cube)
            if found_brick is not None and found_brick != idx:
                return True
        return False

    def add_brick(self, brick):
        idx = len(self.bricks)
        self.bricks.append(brick)
        for cube in brick.cubes:
            assert cube not in self.cubes
            self.cubes[cube] = idx

    def replace_brick(self, idx, new_brick):
        brick = self.bricks[idx]
        for cube in brick.cubes:
            del self.cubes[cube]

        self.bricks[idx] = new_brick
        for cube in new_brick.cubes:
            assert cube not in self.cubes
            self.cubes[cube] = idx


    def show(self, ltr_axis, z_min, z_max):
        assert ltr_axis in [0, 1]

        # Names:
        # - A (or a) is the ltr_axis
        # - B (or b) is the other axis (neither A nor Z, but the other one)

        A = ltr_axis
        B = int(not A)

        foo = {
            (cube[A], cube[Z])
            for brick in self.bricks
            for cube in brick.cubes
        }

        for z in range(z_max, z_min-1, -1):
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

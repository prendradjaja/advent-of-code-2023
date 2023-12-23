#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
'''

import sys
from dataclasses import dataclass
import ast
import functools


X, Y, Z = 0, 1, 2
DOWN = (0, 0, -1)


def main():
    world = CollisionWorld()
    for line in open(sys.argv[1]).read().splitlines():
        start, end = line.split('~')
        start = ast.literal_eval(start)
        end = ast.literal_eval(end)
        world.add_brick(Brick(start, end))

    print('Applying gravity... ', end='', flush=True)
    world.apply_gravity()
    print('Done.')


@dataclass(frozen=True)
class Brick:
    start: ...
    end: ...

    @functools.cached_property
    def cubes(self):
        '''
        Returns the cubes that make up this brick

        >>> Brick((0, 0, 0), (0, 0, 2)).cubes == frozenset([(0, 0, 0), (0, 0, 1), (0, 0, 2)])
        True
        '''
        delta = signvec(subvec(self.end, self.start))
        cubes = [self.start]
        pos = self.start
        while pos != self.end:
            pos = addvec(pos, delta)
            cubes.append(pos)
        return frozenset(cubes)

    def fall_one_unit(self):
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

    def apply_gravity(self):
        while True:
            changed = False
            for i, brick in enumerate(self.bricks):
                if self.brick_can_fall(i):
                    self.replace_brick(i, brick.fall_one_unit())
                    changed = True

            if not changed:
                break

    def brick_can_fall(self, brick_idx):
        brick = self.bricks[brick_idx]
        brick2 = brick.fall_one_unit()
        is_ground_collision = any(
            cube[Z] == 0
            for cube in brick2.cubes
        )
        is_any_collision = is_ground_collision or self.is_collision(brick_idx, brick2)
        return not is_any_collision


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

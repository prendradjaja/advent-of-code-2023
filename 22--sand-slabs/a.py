#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
'''

import sys
from dataclasses import dataclass
import ast


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

    print('Checking each brick... ', end='', flush=True)
    answer = sum(
        1
        for i in range(len(world.bricks))
        if world.can_remove(i)
    )
    print('Done.')

    print('\nAnswer:')
    print(answer)


@dataclass(frozen=True)
class Brick:
    start: ...
    end: ...

    def __post_init__(self):
        '''
        Adds self.cubes (the cubes that make up this brick)

        >>> Brick((0, 0, 0), (0, 0, 2)).cubes == frozenset([(0, 0, 0), (0, 0, 1), (0, 0, 2)])
        True
        '''
        delta = signvec(subvec(self.end, self.start))
        cubes = [self.start]
        pos = self.start
        while pos != self.end:
            pos = addvec(pos, delta)
            cubes.append(pos)
        super().__setattr__('cubes', frozenset(cubes))

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

    def apply_gravity(self, *, _check_stability_only=False):
        '''
        Returns nothing.

        With _check_stability_only=True:
        - Returns truthy if unstable
        - Returns falsy if stable
        '''
        while True:
            changed = False
            for i, brick in enumerate(self.bricks):
                if self.brick_can_fall(i):
                    if _check_stability_only:
                        return 'is-unstable'
                    self.replace_brick(i, brick.fall_one_unit())
                    changed = True

            if not changed:
                break

    def is_stable(self):
        return not self.apply_gravity(_check_stability_only=True)

    def brick_can_fall(self, brick_idx):
        brick = self.bricks[brick_idx]
        brick2 = brick.fall_one_unit()
        is_ground_collision = any(
            cube[Z] == 0
            for cube in brick2.cubes
        )
        is_any_collision = is_ground_collision or self.is_collision(brick_idx, brick2)
        return not is_any_collision

    def can_remove(self, brick_idx):
        # "Hide" the given brick for collision detection
        for cube in self.bricks[brick_idx].cubes:
            del self.cubes[cube]

        result = self.is_stable()

        # Unhide the brick
        for cube in self.bricks[brick_idx].cubes:
            assert cube not in self.cubes
            self.cubes[cube] = brick_idx

        return result


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

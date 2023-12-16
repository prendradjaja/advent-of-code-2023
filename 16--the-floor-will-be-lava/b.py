#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys
from collections import namedtuple


Photon = namedtuple('Photon', 'pos vel')

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def main():
    world = open(sys.argv[1]).read().splitlines()

    HEIGHT = len(world)
    WIDTH = len(world[0])

    possible_initial_photons = (
        [Photon((r, 0), RIGHT) for r in range(HEIGHT)] +
        [Photon((r, WIDTH - 1), LEFT) for r in range(HEIGHT)] +
        [Photon((0, c), DOWN) for c in range(WIDTH)] +
        [Photon((HEIGHT - 1, c), UP) for c in range(WIDTH)]
    )

    answer = max(
        simulate(world, each)
        for each in possible_initial_photons
    )
    print(answer)


def simulate(world, initial_photon):
    photons = set()
    new_photons = {initial_photon}

    while new_photons:
        photons |= new_photons
        new_photons = {
            p2
            for p1 in new_photons
            for p2 in step(p1, world)
        } - photons

    return len({p.pos for p in photons})


def step(photon, world):
    HEIGHT = len(world)
    WIDTH = len(world[0])

    r, c = photon.pos
    ch = world[r][c]

    if ch == '.':
        new_photons = [photon._replace(pos = addvec(photon.pos, photon.vel))]
    elif ch in '/\\':
        new_photons = reflect(photon, ch)
    elif ch in '-|':
        new_photons = split(photon, ch)

    # Exclude any photons that fall off the edge of the world
    return [
        p
        for p in new_photons
        if 0 <= p.pos[0] < HEIGHT
        and 0 <= p.pos[1] < WIDTH
    ]


def reflect(photon, ch):
    case = photon.vel, ch
    if case == (RIGHT, '/'):
        vel = UP
    elif case == (RIGHT, '\\'):
        vel = DOWN
    elif case == (LEFT, '/'):
        vel = DOWN
    elif case == (LEFT, '\\'):
        vel = UP
    elif case == (UP, '/'):
        vel = RIGHT
    elif case == (UP, '\\'):
        vel = LEFT
    elif case == (DOWN, '/'):
        vel = LEFT
    elif case == (DOWN, '\\'):
        vel = RIGHT
    else:
        raise Exception('unreachable case')
    return [photon._replace(
        pos = addvec(photon.pos, vel),
        vel = vel
    )]


def split(photon, ch):
    if (
        photon.vel in [LEFT, RIGHT] and ch == '-' or
        photon.vel in [UP, DOWN] and ch == '|'
    ):
        return [photon._replace(pos = addvec(photon.pos, photon.vel))]
    elif ch == '-':
        assert photon.vel in [UP, DOWN]
        return [
            photon._replace(
                pos = addvec(photon.pos, LEFT),
                vel = LEFT
            ),
            photon._replace(
                pos = addvec(photon.pos, RIGHT),
                vel = RIGHT
            ),
        ]
    elif ch == '|':
        assert photon.vel in [LEFT, RIGHT]
        return [
            photon._replace(
                pos = addvec(photon.pos, UP),
                vel = UP
            ),
            photon._replace(
                pos = addvec(photon.pos, DOWN),
                vel = DOWN
            ),
        ]
    else:
        raise Exception('unreachable case')


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


if __name__ == '__main__':
    main()

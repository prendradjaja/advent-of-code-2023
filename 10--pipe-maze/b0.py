#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys


DIRECTIONS = [
    UP := (-1, 0),
    RIGHT := (0, 1),
    DOWN := (1, 0),
    LEFT := (0, -1),
]

PIPE_DIRECTIONS = {
    '|': [UP, DOWN],
    '-': [LEFT, RIGHT],
    'F': [DOWN, RIGHT],
    '7': [DOWN, LEFT],
    'L': [UP, RIGHT],
    'J': [UP, LEFT],
}


def main():
    def bfs(node):
        visit(node, None)
        visited.add(node)
        q = [node]
        while q:
            node = q.pop(0)
            for v in neighbors(node):
                if v not in visited:
                    visit(v, node)
                    visited.add(v)
                    q.append(v)
    def visit(node, parent):
        plain_world[node] = getitem(world, node)
        distances[node] = distances[parent] + 1
    def neighbors(node):
        ch = getitem(world, node)
        if ch == 'S':
            ch = get_start_tile_type()
        directions = PIPE_DIRECTIONS[ch]
        for d in directions:
            npos = addvec(node, d)
            yield npos


    world = open(sys.argv[1]).read().splitlines()
    for pos, ch in enumerate2d(world):
        if ch == 'S':
            start_pos = pos

    plain_world = {}
    visited = set()
    distances = { None: -1, start_pos: 0 }

    bfs(start_pos)

    def mark_empty(pos, mark):
        if plain_world.get(pos, '.') == '.':
            plain_world[pos] = mark

    pos = start_pos
    del visited
    visited2 = set()
    while True:
        my_neighbors = sorted(npos for npos in neighbors(pos) if npos not in visited2)
        visited2.add(pos)
        if my_neighbors:
            new_pos = my_neighbors[0]
            offset = subvec(new_pos, pos)

            # Mark neighbors before moving
            mark_empty(addvec(pos, rotate_left(offset)), 'a')
            mark_empty(addvec(pos, rotate_right(offset)), 'b')

            # Move
            pos = new_pos

            # Mark neighbors after moving
            mark_empty(addvec(pos, rotate_left(offset)), 'a')
            mark_empty(addvec(pos, rotate_right(offset)), 'b')

        else:
            break
    assert start_pos in neighbors(pos)

    def flood_fill(pos):
        plain_world[pos] = 'a'
        # TODO Do some renaming and/or namespacing to fix the "surroundings is similar to neighbors" thing
        surroundings = [addvec(offset, pos) for offset in DIRECTIONS]
        for npos in surroundings:
            if plain_world.get(npos, '.') == '.':
                flood_fill(npos)

    seeds = [pos for pos, ch in plain_world.items() if ch == 'a']
    for seed in seeds:
        flood_fill(seed)

    for r in range(len(world)):
        for c in range(len(world[0])):
            ch = plain_world.get((r, c), '.')
            print(ch, end='')
        print()

    # TODO Write code for the rest of this problem


def rotate_right(direction):
    n = len(DIRECTIONS)
    return DIRECTIONS[(DIRECTIONS.index(direction) + 1) % n]


def rotate_left(direction):
    n = len(DIRECTIONS)
    return DIRECTIONS[(DIRECTIONS.index(direction) - 1) % n]



def get_start_tile_type():
    # TODO Un-hardcode this
    if sys.argv[1] == 'ex':
        return 'F'
    elif sys.argv[1] == 'ex2':
        return 'F'
    else:
        assert sys.argv[1] == 'in'
        return '|'


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


def subvec(v, w):
    return tuple(a - b for a, b in zip(v, w))


def getitem(grid, pos):
    r, c = pos
    assert (
        0 <= r < len(grid) and
        0 <= c < len(grid[0])
    )
    return grid[r][c]


def enumerate2d(grid):
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            yield (r, c), value


if __name__ == '__main__':
    main()

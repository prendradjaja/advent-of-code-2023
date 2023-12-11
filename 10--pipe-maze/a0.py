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

PIPES = '|-LJ7F'

LEGAL_DIRECTIONS = {
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
        plain_world[node] = getindex(world, node)
        distances[node] = distances[parent] + 1
    def neighbors(node):
        ch = getindex(world, node)
        if ch == 'S':
            ch = get_start_tile_type()
        directions = LEGAL_DIRECTIONS[ch]
        for d in directions:
            npos = addvec(node, d)
            yield npos
            # if getindex(world, npos) == LEGAL_PIPES[ch][d]:


    world = open(sys.argv[1]).read().splitlines()
    for pos, ch in enumerate2d(world):
        if ch == 'S':
            start_pos = pos

    plain_world = {}
    visited = set()
    distances = { None: -1, start_pos: 0 }

    bfs(start_pos)

    for r in range(len(world)):
        for c in range(len(world[0])):
            ch = plain_world.get((r, c), '.')
            print(ch, end='')
        print()

    answer = max(distances.values())
    print(answer)


def get_start_tile_type():
    # TODO Un-hardcode this
    if sys.argv[1] == 'ex':
        return 'F'
    elif sys.argv[1] == 'in':
        return '|'
    else:
        raise Exception('not expected')


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


def getindex(grid, pos):
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

#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys


UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

# DIRECTIONS = [
#     UP := (-1, 0),
#     RIGHT := (0, 1),
#     DOWN := (1, 0),
#     LEFT := (0, -1),
# ]

PIPE_DIRECTIONS = {
    '|': [UP, DOWN],
    '-': [LEFT, RIGHT],
    'F': [DOWN, RIGHT],
    '7': [DOWN, LEFT],
    'L': [UP, RIGHT],
    'J': [UP, LEFT],
}


def main():
    world = [list(line) for line in open(sys.argv[1]).read().splitlines()]

    # Find and replace start pipe
    for pos, ch in enumerate2d(world):
        if ch == 'S':
            start_pos = pos
    start_pipe = get_start_tile_type()
    setindex(world, start_pos, start_pipe)

    # Solve
    distances = find_distances_bfs(world, start_pos)
    answer = max(distances.values())
    print(answer)


def find_distances_bfs(world, node):
    def visit(node, parent):
        # plain_world[node] = getindex(world, node)
        distances[node] = distances[parent] + 1

    # plain_world = {}
    distances = { None: -1 }
    visited = set()
    visit(node, None)
    visited.add(node)
    q = [node]
    while q:
        node = q.pop(0)
        for v in get_connected_pipes(world, node):
            if v not in visited:
                visit(v, node)
                visited.add(v)
                q.append(v)

    # for r in range(len(world)):
    #     for c in range(len(world[0])):
    #         ch = plain_world.get((r, c), '.')
    #         print(ch, end='')
    #     print()

    return distances


def get_connected_pipes(world, pos):
    ch = getindex(world, pos)
    return [addvec(pos, d) for d in PIPE_DIRECTIONS[ch]]


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


def setindex(grid, pos, value):
    r, c = pos
    assert (
        0 <= r < len(grid) and
        0 <= c < len(grid[0])
    )
    grid[r][c] = value


def enumerate2d(grid):
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            yield (r, c), value


if __name__ == '__main__':
    main()

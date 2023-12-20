#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys
from collections import namedtuple

# TODO Make my own implementation of Dijkstra's algorithm
from dijkstra_gribouillis import Dijkstra


Node = namedtuple('Node', 'pos last_direction repeat_count')

DIRECTIONS = [
    UP := (-1, 0),
    DOWN := (1, 0),
    LEFT := (0, -1),
    RIGHT := (0, 1),
]

REPEAT_LIMIT = 3

# TODO Change start node representation. Add a special case to neighbors

def main():
    def neighbors(node):
        if node.pos == (height - 1, width - 1):
            yield (0, 'end', None)
            return

        for offset in DIRECTIONS:
            new_pos = addvec(node.pos, offset)
            is_opposite_direction = (0, 0) == addvec(node.last_direction, offset)
            if not in_bounds(world, new_pos):
                continue
            if is_opposite_direction:
                continue
            if offset != node.last_direction:
                new_node = Node(
                    new_pos,
                    offset,
                    1
                )
                distance = getindex(world, new_pos)
                yield (distance, new_node, None)
            else:
                if node.repeat_count == REPEAT_LIMIT:
                    continue
                else:
                    new_node = node._replace(
                        pos = new_pos,
                        repeat_count = node.repeat_count + 1
                    )
                    distance = getindex(world, new_pos)
                    yield (distance, new_node, None)

    world = [
        [int(n) for n in line]
        for line in open(sys.argv[1]).read().splitlines()
    ]
    start = Node(
        (0, 0),
        DOWN,
        0
    )
    target = 'end'

    height = len(world)
    width = len(world[0])

    d = Dijkstra(
        start,
        neighbors,
        maxitems=None,
        maxdist=None,
        target=target
    )

    assert d.is_shortest(target)
    print(d[target].dist)


def in_bounds(grid, pos):
    r, c = pos
    return (
        0 <= r < len(grid) and
        0 <= c < len(grid[0])
    )


def getindex(grid, pos):
    assert in_bounds(grid, pos)
    r, c = pos
    return grid[r][c]


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


if __name__ == '__main__':
    main()

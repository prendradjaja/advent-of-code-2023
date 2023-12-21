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

REPEAT_MINIMUM = 4
REPEAT_LIMIT = 10


def main():
    def neighbors(node):
        '''
        A node is represented as

        - the string 'start', or
        - the string 'end', or
        - a Node object
        '''
        if node == 'start':
            for direction in [DOWN, RIGHT]:
                pos = direction
                new_node = Node(
                    pos,
                    direction,
                    1
                )
                distance = getitem(world, pos)
                yield (distance, new_node, None)
            return

        if node.pos == (height - 1, width - 1) and node.repeat_count >= REPEAT_MINIMUM:
            yield (0, 'end', None)
            return

        keep_going_node = node._replace(
            pos = addvec(node.pos, node.last_direction),
            repeat_count = node.repeat_count + 1
        )
        turn_directions = [
            d for d in DIRECTIONS
            if d != node.last_direction
            and (0, 0) != addvec(node.last_direction, d)
        ]
        assert len(turn_directions) == 2
        turn_nodes = [
            Node(
                addvec(node.pos, offset),
                offset,
                1
            )
            for offset in turn_directions
            if in_bounds(world, addvec(node.pos, offset))
        ]

        if node.repeat_count < REPEAT_MINIMUM:
            if in_bounds(world, keep_going_node.pos):
                yield (
                    getitem(world, keep_going_node.pos),
                    keep_going_node,
                    None
                )

        elif node.repeat_count == REPEAT_LIMIT:
            yield from (
                (
                    getitem(world, each.pos),
                    each,
                    None
                )
                for each in turn_nodes
                if in_bounds(world, each.pos)
            )

        else:
            assert node.repeat_count < REPEAT_LIMIT
            if in_bounds(world, keep_going_node.pos):
                yield (
                    getitem(world, keep_going_node.pos),
                    keep_going_node,
                    None
                )
            yield from (
                (
                    getitem(world, each.pos),
                    each,
                    None
                )
                for each in turn_nodes
                if in_bounds(world, each.pos)
            )

    world = [
        [int(n) for n in line]
        for line in open(sys.argv[1]).read().splitlines()
    ]
    start = 'start'
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


def getitem(grid, pos):
    assert in_bounds(grid, pos)
    r, c = pos
    return grid[r][c]


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


if __name__ == '__main__':
    main()

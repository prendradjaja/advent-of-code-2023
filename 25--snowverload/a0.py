#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys
import collections
import itertools
import random
import math


# Maybe use Graphviz?
# https://old.reddit.com/r/adventofcode/comments/18qcer7/2023_day_25_graphviz_rescues_once_again/


def main():
    sys.setrecursionlimit(100_000)

    g = Graph()
    for line in open(sys.argv[1]).read().splitlines():
        left, rights = line.split(': ')
        rights = rights.split()
        for right in rights:
            g.add_edge(left, right)

    # g.remove_edge('hfx', 'pzl')
    # g.remove_edge('bvb', 'cmg')
    # g.remove_edge('nvd', 'jqt')

    # print(len(find_connected_components(g)))
    # print(len(g.vertices))

    print(f'{len(g.vertices)=}')
    print()

    h = pick_initial_subgraph(g)
    h = discard_others(g, h)
    ccs = find_connected_components(h)
    cc0, cc1 = ccs
    [[rep1, *_], [rep2, *_]] = ccs
    print(f'{len(h.vertices)=}')

    for i in range(24):
        h2 = iterate(g, h, rep1, rep2)
        if not h2:
            break
        h = h2
        h = discard_others(g, h)
        ccs = find_connected_components(h)
        cc0, cc1 = ccs
        print(f'{i} {len(h.vertices)=}', end=' ', flush=True)

    print()
    cutoff = 1482
    if len(h.vertices) < cutoff:
        print(f'len(h.vertices) is too low ({len(h.vertices)}, required {cutoff}). This is an expected possibility for this probabilistic approach.')
        print('Try re-running.')
        exit()

    # cc_lengths = sorted(
    #     (len(comp) for comp in find_connected_components(h)),
    #     reverse=True
    # )
    # print(cc_lengths)

    remaining_edges = set(g.get_edges()) - set(h.get_edges())
    print('# of candidate edges:', len(remaining_edges))
    print('Max possible number of iterations:', math.comb(len(remaining_edges), 3))

    candidate_edges = list(remaining_edges)

    for i, (e1, e2, e3) in enumerate(itertools.combinations(candidate_edges, 3)):
        if i % 1000 == 0:
            print(f'... {i:,}')

        g.remove_edge(*e1)
        g.remove_edge(*e2)
        g.remove_edge(*e3)

        ccs = find_connected_components(g)
        if len(ccs) == 2:
            cc1, cc2 = ccs
            print('Answer:')
            print(len(cc1) * len(cc2))
            exit()
        elif len(ccs) != 1:
            raise Exception('unexpected')

        g.add_edge(*e1)
        g.add_edge(*e2)
        g.add_edge(*e3)

    print('Failed to find the answer! Not sure why this case happens sometimes.')
    print('Try re-running.')


def discard_others(g, h):
    '''Keep only the two biggest components'''
    return get_subgraph(g, get_biggest_components(h))


def is_connected(g, a, b):
    def dfs(v, visited=None):
        nonlocal found

        if v == b:
            found = True

        if visited is None:
            visited = set()
        visited.add(v)
        for neighbor in g.neighbors[v]:
            if neighbor not in visited:
                dfs(neighbor, visited)

    found = False
    dfs(a)
    return found


def iterate(g, h, rep1, rep2):
    for _ in range(20):
        print('.', end='', flush=True)
        unpicked_vertices = list(set(g.vertices) - set(h.vertices))
        # n = min(len(unpicked_vertices), 25)
        n = len(unpicked_vertices) // 5
        some_vertices = random.sample(unpicked_vertices, n) + list(h.vertices)
        # except ValueError:
        #     raise
        h2 = get_subgraph(g, some_vertices)
        items = sorted(
            (len(comp) for comp in find_connected_components(h2)),
            reverse=True
        )
        if not is_connected(h2, rep1, rep2) and len(h2.vertices) > len(h.vertices):
            print()
            return h2
    print('Stopped after too many tries')
    return None


def get_biggest_components(g2):
    a, b, *rest = sorted(
        find_connected_components(g2),
        key=len,
        reverse=True
    )
    return a + b


def pick_initial_subgraph(g):
    while True:
        some_vertices = random.sample(list(g.vertices), 500)
        g2 = get_subgraph(g, some_vertices)
        a, b, c, *rest = sorted(
            (len(comp) for comp in find_connected_components(g2)),
            reverse=True
        )
        if b > 3 * c and a < 2 * b:
            return g2


# def get_bridge_probability(g, g2):
#     all_edges = len(g.get_edges())
#     some_edges = len(g2.get_edges())


def get_subgraph(g, vertices):
    assert len(vertices) == len(set(vertices))
    g2 = Graph()
    for v in vertices:
        for w in g.neighbors[v]:
            if w in vertices:
                g2.add_edge(v, w)
    return g2


def find_connected_components(g):
    def dfs(vertex, visited=None):
        # Visit
        to_connect.remove(vertex)
        group.append(vertex)

        if visited is None:
            visited = set()
        visited.add(vertex)
        for neighbor in g.neighbors[vertex]:
            if neighbor not in visited:
                dfs(neighbor, visited)

    to_connect = set(g.vertices)
    groups = []
    while to_connect:
        group = []
        groups.append(group)
        vertex = next(iter(to_connect))
        dfs(vertex)
    return groups


class Graph:
    def __init__(self):
        self.neighbors = collections.defaultdict(set)
        self.vertices = self.neighbors.keys()

    def add_edge(self, v, w):
        '''Adds the given edge (does nothing if that edge already exists)'''
        self.neighbors[v].add(w)
        self.neighbors[w].add(v)

    def remove_edge(self, v, w):
        '''Removes the given edge (raises an error if that edge does not
        exist)'''
        self.neighbors[v].remove(w)
        self.neighbors[w].remove(v)

    def get_edges(self):
        edges = set()
        for v in self.neighbors:
            for w in self.neighbors[v]:
                edge = tuple(sorted([v, w]))
                edges.add(edge)
        return list(edges)


if __name__ == '__main__':
    main()

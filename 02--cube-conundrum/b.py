#!/usr/bin/env python3.12
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

from sscanf import sscanf

from collections import Counter
import sys
from operator import or_
from functools import reduce
import math


def main():
    # min_possible[N] = Counter({ 'red': R, 'green': G, 'blue': B }) means:
    # For Game N, there must be at least R red cubes, G green, and B blue.
    min_possible = {}
    for line in open(sys.argv[1]).read().splitlines():
        template = 'Game %u: %s'
        gid, observations_text = sscanf(line, template)
        observations = [
            parse_observation(each)
            for each in observations_text.split('; ')
        ]
        min_possible[gid] = reduce(or_, observations)

    answer = sum(
        math.prod(bag.values())
        for bag in min_possible.values()
    )
    print(answer)


def parse_observation(obs):
    result = {}
    for part in obs.split(', '):
        n, color = part.split()
        n = int(n)
        result[color] = n
    return Counter(result)


if __name__ == '__main__':
    main()

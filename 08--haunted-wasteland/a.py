#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
'''

from sscanf import sscanf

import sys
import itertools


def main():
    # Parse
    sections = open(sys.argv[1]).read().split('\n\n')
    instructions, network_text = sections

    network = {}
    for line in network_text.splitlines():
        curr, left, right = sscanf(line, '%s = (%s, %s)')
        network[curr] = {'L': left, 'R': right}

    # Simulate
    curr = 'AAA'
    n = 0
    instructions = itertools.cycle(instructions)
    while curr != 'ZZZ':
        n += 1
        curr = network[curr][next(instructions)]

    print(n)


if __name__ == '__main__':
    main()

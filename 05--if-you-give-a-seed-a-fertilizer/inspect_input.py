#!/usr/bin/env python3
'''
Usage:
    ./inspect_input.py PATH_TO_EXAMPLE_INPUT_FILE
    ./inspect_input.py PATH_TO_PUZZLE_INPUT_FILE
'''

import sys
import itertools


def main():
    global n

    n = 0

    # Read file and split into sections
    text = open(sys.argv[1]).read().strip()
    sections = text.split('\n\n')
    _, *map_texts = sections

    for text in map_texts:
        inspect_map(text.splitlines()[1:])

    print(f'{n} combinations inspected. No overlaps found.')


def inspect_map(lines):
    global n

    ranges = {}
    for line in lines:
        dst_start, src_start, range_length = [int(n) for n in line.split()]
        src_range = range(src_start, src_start + range_length)
        dst_range = range(dst_start, dst_start + range_length)
        ranges[src_range] = dst_range

    for r1, r2 in itertools.combinations(ranges.keys(), 2):
        n += 1
        assert not is_overlap(r1, r2)

    for r1, r2 in itertools.combinations(ranges.values(), 2):
        n += 1
        assert not is_overlap(r1, r2)


def is_overlap(range1, range2):
    '''
    >>> is_overlap(range(1, 5), range(3, 7))
    True
    >>> is_overlap(range(3, 7), range(1, 5))
    True
    >>> is_overlap(range(1, 7), range(3, 5))
    True
    >>> is_overlap(range(1, 5), range(6, 7))
    False
    >>> is_overlap(range(1, 5), range(5, 7))
    False
    '''
    range1, range2 = sorted([range1, range2], key=lambda r: r[0])
    return range2[0] in range1


if __name__ == '__main__':
    main()

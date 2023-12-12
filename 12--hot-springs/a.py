#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
'''

import sys
import itertools


def main():
    answer = sum(
        count_arrangements(line)
        for line in open(sys.argv[1]).read().splitlines()
    )
    print(answer)


def count_arrangements(line):
    conditions, groups_text = line.split()
    groups = [int(n) for n in groups_text.split(',')]
    count_known_damaged = sum(1 for ch in conditions if ch == '#')
    count_damaged = sum(groups)
    count_unknown = sum(1 for ch in conditions if ch == '?')

    result = 0
    for indices in itertools.combinations(
        range(count_unknown),
        count_damaged - count_known_damaged  # How many slots do we need to fill?
    ):
        filled = fill_slots(conditions, indices)
        if to_groups(filled) == groups:
            result += 1

    return result


def to_groups(conditions):
    '''
    >>> to_groups('.#.###.#.######')
    [1, 3, 1, 6]
    '''
    result = []
    for k, g in itertools.groupby(conditions):
        if k == '#':
            result.append(len(list(g)))
    return result


def fill_slots(template, damaged_indices):
    '''
    Fill the given indices with '#' and fill the rest with '.'

    >>> fill_slots('??..##??', [0, 3])
    '#...##.#'
    '''
    slot_values = (
        '#' if n in damaged_indices else '.'
        for n in itertools.count()
    )
    s = ''
    for ch in template:
        if ch == '?':
            s += next(slot_values)
        else:
            s += ch
    return s


if __name__ == '__main__':
    main()

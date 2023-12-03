#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys
import re
import string
from collections import namedtuple


PartNumber = namedtuple('PartNumber', 'value left_endpoint right_endpoint')


def main():
    schematic = open(sys.argv[1]).read().splitlines()
    part_numbers = []
    for r, row in enumerate(schematic):
        for start, end in find_numbers(row):
            n = int(row[start : end+1])
            part_numbers.append(
                PartNumber(n, (r, start), (r, end))
            )

    answer = sum(
        each.value
        for each in part_numbers
        if any(is_symbol(neighbor) for neighbor in neighbors(schematic, each))
    )

    print(answer)


def is_symbol(ch):
    return (
        ch not in string.digits
        and ch != '.'
    )


def find_numbers(line):
    start = None
    results = []
    for i, ch in enumerate(line + '!'):
        if ch not in string.digits and start is not None:
            results.append((start, i - 1))
            start = None
        elif ch in string.digits and start is None:
            start = i
    return results


def neighbors(schematic, part_number):
    HEIGHT = len(schematic)
    WIDTH = len(schematic[0])

    positions = []
    R, start = part_number.left_endpoint
    _, end = part_number.right_endpoint
    for c in range(start - 1, end + 2):
        positions.append((R - 1, c))
        positions.append((R + 1, c))
    positions.append((R, start - 1))
    positions.append((R, end + 1))

    for r, c in positions:
        if (
            0 <= r < HEIGHT and
            0 <= c < WIDTH
        ):
            yield schematic[r][c]


if __name__ == '__main__':
    main()

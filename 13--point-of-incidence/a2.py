#!/usr/bin/env python3
'''
Look at `diff a2.py b.py`, not `diff a.py b.py`.

Usage:
    ./a.py PATH_TO_INPUT_FILE
'''

import sys


def main():
    patterns = [
        paragraph.splitlines()
        for paragraph in open(sys.argv[1]).read().split('\n\n')
    ]

    answer = sum(
        find_axis_number(each)
        for each in patterns
    )
    print(answer)


def find_axis_number(pattern):
    has_horizontal_axis, axis = find_horizontal_axis(pattern)
    if has_horizontal_axis:
        return 100 * axis

    has_vertical_axis, axis = find_vertical_axis(pattern)
    if has_vertical_axis:
        return axis

    return 0


def find_horizontal_axis(pattern):
    def axis_is(axis):
        for r1, r2 in zip(
            range(axis, len(pattern)),
            range(axis - 1, -1, -1)
        ):
            if pattern[r1] != pattern[r2]:
                return False
        return True

    pattern = [''.join(line) for line in pattern]
    for axis in range(1, len(pattern)):
        if axis_is(axis):
            return (True, axis)

    return (False, None)


def find_vertical_axis(pattern):
    return find_horizontal_axis(transpose(pattern))


def transpose(m):
    """
    >>> transpose([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]
    """
    return [list(i) for i in zip(*m)]


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys


def main():
    patterns = [
        paragraph.splitlines()
        for paragraph in open(sys.argv[1]).read().split('\n\n')
    ]

    answer = 0
    for each in patterns:
        has_horizontal_axis, axis = find_horizontal_axis(each)
        if has_horizontal_axis:
            answer += 100 * axis
            continue

        has_vertical_axis, axis = find_vertical_axis(each)
        if has_vertical_axis:
            answer += axis
    print(answer)


def find_horizontal_axis(pattern):
    def axis_is(axis):

        def print(*args):
            pass

        print()
        print(axis)
        for r1, r2 in zip(
            range(axis, len(pattern)),
            range(axis - 1, -1, -1)
        ):
            print('.', r1, r2)
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


def flipvert(m):
    """
    >>> flipvert([[1, 2], [3, 4]])
    [[3, 4], [1, 2]]
    """
    return m[::-1]


def fliphorz(m):
    """
    >>> fliphorz([[1, 2], [3, 4]])
    [[2, 1], [4, 3]]
    """
    return transpose(flipvert(transpose(m)))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys


def main():
    grid = open(sys.argv[1]).read().splitlines()

    transposed = transpose(grid)
    for i, row in enumerate(transposed):
        transposed[i] = '#'.join(
            tilt_west(each)
            for each in ''.join(row).split('#')
        )

    answer = sum(
        i
        for row in transposed
        for i, ch in enumerate(reversed(row), start=1)
        if ch == 'O'
    )
    print(answer)


def tilt_west(s):
    return ''.join(sorted(s, reverse=True))


def transpose(m):
    """
    >>> transpose([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]
    """
    return [list(i) for i in zip(*m)]


if __name__ == '__main__':
    main()

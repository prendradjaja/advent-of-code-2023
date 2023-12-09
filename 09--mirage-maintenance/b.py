#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys


def main():
    xss = [
        [int(x) for x in line.split()]
        for line in open(sys.argv[1]).read().splitlines()
    ]
    answer = sum(extrapolate(xs[::-1]) for xs in xss)
    print(answer)


def diffs(xs):
    return [
        b - a
        for a, b
        in zip(xs, xs[1:])
    ]


def extrapolate(xs):
    if all(x == 0 for x in xs):
        return 0
    next_diff = extrapolate(diffs(xs))
    return xs[-1] + next_diff


if __name__ == '__main__':
    main()

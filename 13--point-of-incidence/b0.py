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
    for i, each in enumerate(patterns):
        print(i)
        axis_number = find_smudged_axis_number(each)
        answer += axis_number
    print('answer')
    print(answer)

    # print(find_smudged_axis_number(patterns[7]))
    # pattern = patterns[7]
    # flipped = flip(pattern, (8, 8))
    # print(find_axis_number(flipped))


def find_smudged_axis_number(pattern):
    for row in pattern:
        print(row)

    print('---')

    old_axis_number = find_axis_number(pattern)
    print('old', old_axis_number)
    for r in range(len(pattern)):
        for c in range(len(pattern[0])):
            flipped = flip(pattern, (r, c))
            # for row in flipped:
            #     print(row)
            # print()
            new_axis_number = find_axis_number(flipped, ignore=old_axis_number)
            if new_axis_number and (new_axis_number != old_axis_number):
                return new_axis_number
    raise Exception('No smudge found')


def flip(pattern, pos):
    def flip_symbol(symbol):
        if symbol == '.':
            return '#'
        else:
            assert symbol == '#'
            return '.'

    R, C = pos
    new_pattern = []
    for r, row in enumerate(pattern):
        if r == R:
            new_pattern.append(
                row[:C]
                + flip_symbol(row[C])
                + row[C + 1:]
            )
        else:
            new_pattern.append(row)
    return new_pattern


def find_axis_number(pattern, ignore=0):
    has_horizontal_axis, axis = find_horizontal_axis(pattern, ignore=ignore//100)
    if has_horizontal_axis:
        return 100 * axis

    has_vertical_axis, axis = find_vertical_axis(pattern, ignore=ignore)
    if has_vertical_axis:
        return axis

    return 0


def find_horizontal_axis(pattern, ignore=0):
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
        if axis_is(axis) and axis != ignore:
            return (True, axis)
    return (False, None)


def find_vertical_axis(pattern, ignore=0):
    return find_horizontal_axis(transpose(pattern), ignore=ignore)


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

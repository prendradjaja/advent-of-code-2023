#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

from sscanf import sscanf

import sys


def main():
    winning_sets = []
    chosen_sets = []
    for line in open(sys.argv[1]).read().splitlines():
        _, winning_set, chosen_set = sscanf(line, 'Card %s: %s | %s')
        winning_set = {int(n) for n in winning_set.strip().split()}
        chosen_set = {int(n) for n in chosen_set.strip().split()}
        winning_sets.append(winning_set)
        chosen_sets.append(chosen_set)

    answer = 0
    for winners, chosen in zip(winning_sets, chosen_sets):
        matches = len(winners & chosen)
        if matches:
            points = 2 ** (matches - 1)
        else:
            points = 0
        answer += points

    print(answer)


if __name__ == '__main__':
    main()

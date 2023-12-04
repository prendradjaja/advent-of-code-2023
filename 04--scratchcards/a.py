#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

from sscanf import sscanf

import sys
from dataclasses import dataclass


def main():
    cards = []
    for line in open(sys.argv[1]).read().splitlines():
        _, winners, chosen = sscanf(line, 'Card %s: %s | %s')
        winners = {int(n) for n in winners.strip().split()}
        chosen = {int(n) for n in chosen.strip().split()}
        cards.append(Card(winners, chosen))

    answer = 0
    for card in cards:
        matches = len(card.winners & card.chosen)
        if matches:
            points = 2 ** (matches - 1)
        else:
            points = 0
        answer += points

    print(answer)


@dataclass
class Card:
    winners: set[int]
    chosen: set[int]


if __name__ == '__main__':
    main()

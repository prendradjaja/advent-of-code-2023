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

    # Because each card affects only the cards after it, we can process cards
    # in one forward pass
    for i, card in enumerate(cards):
        next_idx = i + 1
        for j in range(next_idx, next_idx + card.matches):
            # Copy cards[j] once for every copy of cards[i]
            cards[j].count += card.count

    answer = sum(card.count for card in cards)
    print(answer)


@dataclass
class Card:
    winners: set[int]
    chosen: set[int]

    def __post_init__(self):
        self.count = 1
        self.matches = len(self.winners & self.chosen)


if __name__ == '__main__':
    main()

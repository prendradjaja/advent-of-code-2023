#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
'''

import sys
from collections import namedtuple, Counter
from enum import Enum, auto


Hand = namedtuple('Hand', 'cards bid')


class HandType(Enum):
    # From weakest to strongest
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


def main():
    hands = []
    for line in open(sys.argv[1]).read().splitlines():
        cards, bid = line.split()
        bid = int(bid)
        hands.append(Hand(cards, bid))

    sorted_hands = sorted(
        hands,
        key = lambda hand: (
            get_hand_type(hand.cards).value,
            [get_card_value(card) for card in hand.cards]
        )
    )

    answer = sum(
        rank * hand.bid
        for rank, hand in enumerate(sorted_hands, start=1)
    )
    print(answer)


def get_hand_type(cards):
    counts = sorted(Counter(cards).values(), reverse=True)
    if counts == [5]:
        return HandType.FIVE_OF_A_KIND
    elif counts == [4, 1]:
        return HandType.FOUR_OF_A_KIND
    elif counts == [3, 2]:
        return HandType.FULL_HOUSE
    elif counts == [3, 1, 1]:
        return HandType.THREE_OF_A_KIND
    elif counts == [2, 2, 1]:
        return HandType.TWO_PAIR
    elif counts == [2, 1, 1, 1]:
        return HandType.ONE_PAIR
    elif counts == [1, 1, 1, 1, 1]:
        return HandType.HIGH_CARD
    else:
        raise Exception('unreachable case')


def get_card_value(card):
    try:
        return int(card)
    except ValueError:
        return {
            'A': 14,
            'K': 13,
            'Q': 12,
            'J': 11,
            'T': 10,
        }[card]


if __name__ == '__main__':
    main()

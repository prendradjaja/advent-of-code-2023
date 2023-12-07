#!/usr/bin/env python3
'''
This version has a smallish performance optimization vs b.py (compare
resolve_jokers() implementations).

It's not necessary for solving the puzzle input, but on larger inputs it could
make a difference. Even on the puzzle input, it makes the difference between
0.1sec runtime (b.faster.py) and 1sec runtime (b.py) on my machine.

Another obvious place for further optimization: fill_slots() will turn e.g.
KQTJJ into both KQTKQ and KQTQK, which is not necessary since they are
permutations of each other.


Usage:
    ./b.faster.py PATH_TO_INPUT_FILE
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
    # Parse
    hands = []
    for line in open(sys.argv[1]).read().splitlines():
        cards, bid = line.split()
        bid = int(bid)
        hands.append(Hand(cards, bid))

    # Sort
    sorted_hands = sorted(
        hands,
        key = lambda hand: (
            get_hand_type(resolve_jokers(hand.cards)).value,
            [get_card_value(card) for card in hand.cards]
        )
    )

    # Count winnings
    answer = sum(
        rank * hand.bid
        for rank, hand in enumerate(sorted_hands, start=1)
    )
    print(answer)


def resolve_jokers(cards):
    if 'J' not in cards:
        return cards

    non_jokers = {c for c in cards if c != 'J'}
    choose_from = non_jokers or {'2'}  # 2 is just an arbitrary card
    return max(
        fill_slots(cards, choose_from, 'J'),
        key = lambda cards: get_hand_type(cards).value
    )


def fill_slots(s, choose_from, slot_char):
    '''
    >>> list(fill_slots('ABC', 'abc', '_'))
    ['ABC']
    >>> list(fill_slots('AB_', 'abc', '_'))
    ['ABa', 'ABb', 'ABc']
    >>> list(fill_slots('A__', 'abc', '_'))
    ['Aaa', 'Aab', 'Aac', 'Aba', 'Abb', 'Abc', 'Aca', 'Acb', 'Acc']
    '''
    if slot_char not in s:
        yield s
        return

    idx = s.index(slot_char)
    for choice in choose_from:
        s2 = s[:idx] + choice + s[idx + 1:]
        yield from fill_slots(s2, choose_from, slot_char)


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
            'T': 10,
            'J': 1,
        }[card]


if __name__ == '__main__':
    main()

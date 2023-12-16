#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys
from collections import namedtuple

from sscanf import sscanf


# EqualsStep.type always == '='
EqualsStep = namedtuple('EqualsStep', 'type label focal_length')
# DashStep.type always == '-'
DashStep = namedtuple('DashStep', 'type label')

Lens = namedtuple('Lens', 'label focal_length')


def main():
    steps = [
        parse_step(step)
        for step in open(sys.argv[1]).read().split(',')
    ]

    boxes = { i: [] for i in range(256) }
    for step in steps:
        box = boxes[get_hash(step.label)]
        if step.type == '-':
            remove_by(box, lambda lens: lens.label == step.label)
        elif step.type == '=':
            idx = index_by(box, lambda lens: lens.label == step.label)
            lens = Lens(step.label, step.focal_length)
            if idx is not None:
                box[idx] = lens
            else:
                box.append(lens)

    answer = sum(
        (i + 1) * j * lens.focal_length
        for i, box in boxes.items()
        for j, lens in enumerate(box, start=1)
    )
    print(answer)


def show(boxes):
    def format_lens(lens):
        return f'[{lens.label} {lens.focal_length}]'

    for i, box in boxes.items():
        if box:
            print(f'Box {i} {" ".join(format_lens(lens) for lens in box)}')


def get_hash(s):
    n = 0
    for ch in s:
        n += ord(ch)
        n = (n * 17) % 256
    return n


def parse_step(step):
    match = sscanf(step, '%s=%u')
    if match:
        return EqualsStep('=', *match)

    match = sscanf(step, '%s-')
    if match:
        return DashStep('-', *match)

    raise Exception('parse error ' + step)


def remove_by(lst, pred):
    matches = [i for i, x in enumerate(lst) if pred(x)]
    if len(matches) == 1:
        lst.pop(matches[0])
    elif len(matches) == 0:
        pass
    else:
        raise Exception('unexpected case')


def index_by(lst, pred):
    matches = [i for i, x in enumerate(lst) if pred(x)]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) == 0:
        return None
    else:
        raise Exception('unexpected case')


if __name__ == '__main__':
    main()

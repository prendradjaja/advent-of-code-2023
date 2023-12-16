#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys


def main():
    text = open(sys.argv[1]).read()
    answer = sum(
        get_hash(step)
        for step in text.split(',')
    )
    print(answer)


def get_hash(s):
    n = 0
    for ch in s:
        n += ord(ch)
        n = (n * 17) % 256
    return n


if __name__ == '__main__':
    main()

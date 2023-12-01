#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
'''

import string
import sys


def main():
    answer = 0
    for line in open(sys.argv[1]).read().splitlines():
        digits = [ch for ch in line if ch in string.digits]
        calibration_value = int(
            digits[0] +
            digits[-1]
        )
        answer += calibration_value
    print(answer)


if __name__ == '__main__':
    main()

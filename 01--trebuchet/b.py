#!/usr/bin/env python3
'''
Usage:
    ./b.py PATH_TO_INPUT_FILE
'''

import string
import sys


NUMBERS = {
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


def main():
    answer = 0
    for line in open(sys.argv[1]).read().splitlines():
        digits = []

        for i in range(len(line)):
            for word in NUMBERS:
                if word == line[i : i+len(word)]:
                    digits.append(NUMBERS[word])

        first_digit = digits[0]
        last_digit = digits[-1]

        calibration_value = int(
            first_digit +
            last_digit
        )

        answer += calibration_value

    print(answer)


if __name__ == '__main__':
    main()

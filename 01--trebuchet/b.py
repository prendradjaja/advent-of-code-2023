#!/usr/bin/env python3
'''
Usage:
    ./b.py PATH_TO_INPUT_FILE
'''

import string
import sys


NUMBERS = {
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
        digits = {
            i: ch
            for i, ch in enumerate(line)
            if ch in string.digits
        }

        for word, n in NUMBERS.items():
            for i in indices(line, word):
                assert i not in digits
                digits[i] = n

        first_digit = digits[min(digits)]
        last_digit = digits[max(digits)]

        calibration_value = int(
            first_digit +
            last_digit
        )

        answer += calibration_value

    print(answer)


def indices(haystack, needle):
    '''
    >>> indices('-wowow-', 'wow')
    [1, 3]
    >>> indices('-wowow-', 'nope')
    []
    '''
    result = []
    for i in range(len(haystack)):
        if haystack[i : i+len(needle)] == needle:
            result.append(i)
    return result


if __name__ == '__main__':
    main()

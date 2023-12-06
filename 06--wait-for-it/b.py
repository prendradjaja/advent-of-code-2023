#!/usr/bin/env python3
'''
Usage:
    ./b.py PATH_TO_INPUT_FILE
'''

import sys
import math


def main():
    # Parse
    time_limit, record = open(sys.argv[1]).read().splitlines()
    time_limit = int(''.join(time_limit.split()[1:]))
    record = int(''.join(record.split()[1:]))

    # Simulate
    wins = 0
    for charge_time in range(0, time_limit+1):
        speed = charge_time
        move_time = time_limit - charge_time
        distance = speed * move_time
        if distance > record:
            wins += 1

    # Multiply
    print(wins)


if __name__ == '__main__':
    main()

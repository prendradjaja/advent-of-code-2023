#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
'''

import sys
import math


def main():
    # Parse
    time_limits, records = open(sys.argv[1]).read().splitlines()
    time_limits = [int(n) for n in time_limits.split()[1:]]
    records = [int(n) for n in records.split()[1:]]

    # Simulate
    wins = []
    for time_limit, record in zip(time_limits, records):
        curr_wins = 0
        for charge_time in range(0, time_limit+1):
            speed = charge_time
            move_time = time_limit - charge_time
            distance = speed * move_time
            if distance > record:
                curr_wins += 1
        wins.append(curr_wins)

    # Multiply
    print(math.prod(wins))


if __name__ == '__main__':
    main()

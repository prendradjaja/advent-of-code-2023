#!/usr/bin/env python3
'''
This solution is sufficient for the example input, but too slow for the puzzle
input.

Usage:
    ./a_slow.py PATH_TO_INPUT_FILE
'''

import sys


def main():
    text = open(sys.argv[1]).read().strip()
    sections = text.split('\n\n')
    seeds_text, *map_texts = sections

    # Parse seeds
    seeds = [
        int(n)
        for n in seeds_text.split()[1:]  # Discard first item: It's "seeds:"
    ]

    # Parse maps and turn them into functions
    maps = []
    for map_text in map_texts:
        name_line, *map_lines = map_text.splitlines()
        maps.append(make_map(map_lines))

    # Solve
    locations = []
    for seed in seeds:
        x = seed
        for f in maps:
            x = f(x)
        locations.append(x)
    print(min(locations))


def make_map(lines):
    my_map = {}
    for line in lines:
        dst_start, src_start, range_length = [int(n) for n in line.split()]
        for src, dst in zip(
            range(src_start, src_start + range_length),
            range(dst_start, dst_start + range_length)
        ):
            if src in my_map:
                print('INFO: src already in my_map')
            my_map[src] = dst

    def f(x):
        return my_map.get(x, x)

    return f


if __name__ == '__main__':
    main()

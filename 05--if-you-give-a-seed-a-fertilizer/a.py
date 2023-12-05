#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
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
    ranges = {}
    for line in lines:
        dst_start, src_start, range_length = [int(n) for n in line.split()]
        src_range = range(src_start, src_start + range_length)
        dst_range = range(dst_start, dst_start + range_length)
        ranges[src_range] = dst_range

    def f(x):
        for src_range, dst_range in ranges.items():
            if x in src_range:
                return dst_range[src_range.index(x)]
        return x

    return f


if __name__ == '__main__':
    main()

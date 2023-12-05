#!/usr/bin/env python3
'''
Some observations about this problem: Each "f" (seed-to-soil relation,
soil-to-fertilizer relation) is a function. Also, for each f, none of the
source ranges overlap, and none of the destination ranges overlap. (See
inspect_input.py)

Usage:
    ./b.py PATH_TO_INPUT_FILE
'''

import sys


def main():
    def get_location(seed):
        x = seed
        for f in maps:
            x = f(x)
        return x

    def is_initial_seed(seed):
        return any(seed in r for r in seed_ranges)


    # Read file and split into sections
    text = open(sys.argv[1]).read().strip()
    sections = text.split('\n\n')
    seeds_text, *map_texts = sections

    # Parse seed ranges
    seed_ranges = parse_seed_ranges(seeds_text)

    # Parse maps and turn them into functions
    maps = []
    for map_text in map_texts:
        name_line, *map_lines = map_text.splitlines()
        maps.append(make_map(map_lines))

    # Key idea of the solution: If we were to look at every possible initial
    # seed value, this would take too long. But actually, only some seed
    # values could actually possibly lead to the answer.
    #
    # We can step backwards through the maps to figure out which seed values
    # those are:
    # 1. First, look at the discontinuities in the "humidities to locations"
    #    map. These are our "Interesting Locations."
    # 2. Map those back to humidities, and they are Interesting Humidities.
    #    In addition, we have a few more interesting humidities: the
    #    discontinuities in the "temperature to humidity" map.
    # 3. Repeat step 2 until we have a list of Interesting Seeds. These are
    #    the only seeds we need to inspect.
    interesting_values = []
    for f in maps[::-1]:
        interesting_values.extend(f.interesting_values)
        interesting_values = [f.inverse(x) for x in interesting_values]
    interesting_seeds = interesting_values

    answer = min(get_location(seed) for seed in interesting_values if is_initial_seed(seed))
    print(answer)


def parse_seed_ranges(seeds_text):
    ints = iter(
        int(n)
        for n in seeds_text.split()[1:]  # Discard first item: It's "seeds:"
    )

    result = []
    while True:
        try:
            start, length = next(ints), next(ints)
        except StopIteration:
            break
        result.append(range(start, start + length))

    return result


def make_map(lines):
    ranges = {}
    interesting_values = []
    for line in lines:
        dst_start, src_start, range_length = [int(n) for n in line.split()]
        src_range = range(src_start, src_start + range_length)
        dst_range = range(dst_start, dst_start + range_length)
        ranges[src_range] = dst_range
        interesting_values.extend([dst_start - 1, dst_start, dst_start + range_length - 1, dst_start + range_length])

    def f(x):
        for src_range, dst_range in ranges.items():
            if x in src_range:
                idx = src_range.index(x)
                return dst_range[idx]
        return x

    def f_inverse(x):
        original_x = x
        for src_range, dst_range in ranges.items():
            if x in dst_range:
                idx = dst_range.index(x)
                return src_range[idx]
        return x

    f.inverse = f_inverse

    # Interesting values in the codomain of f
    f.interesting_values = interesting_values

    return f


if __name__ == '__main__':
    main()

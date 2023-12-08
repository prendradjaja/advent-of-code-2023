#!/usr/bin/env python3
'''
Key idea & thought process for this problem:

- "Wait, isn't this really easy? If the original network was small enough to
  run quickly, wouldn't smaller networks result in a fast runtime too?"

- "Oh -- no, this isn't running quickly. There's a trick. What's the trick?"

- Key idea: Looking at the what happens for the example input, we can see that
  "ghost 1" (the one starting at 11A) gets in a cycle of length 2, and "ghost
  2" gets in a cycle of length 3. The end condition is reached when both
  ghosts finish their cycles simultaneously, i.e. after LCM(2, 3) steps.

- Indeed, Eric used the same trick in the puzzle input, combining multiple
  small cycles to make one long cycle that would take too long to simulate in
  full.

Fun fact: This trick (multiple cycles combining together to make one very-long
cycle) has been used at least once before in Advent of Code: (spoiler for a
past year, decode with rot13) lrne gjragl avargrra qnl gjryir cneg gjb


Usage:
    ./b.py PATH_TO_INPUT_FILE
'''

from sscanf import sscanf

import sys
import itertools
import math


def main():
    # Parse
    sections = open(sys.argv[1]).read().split('\n\n')
    instructions, network_text = sections

    network = {}
    for line in network_text.splitlines():
        curr, left, right = sscanf(line, '%s = (%s, %s)')
        network[curr] = {'L': left, 'R': right}

    # Solve
    start_nodes = [node for node in network if node.endswith('A')]
    answer = math.lcm(*[
        get_cycle_length(node, instructions, network)
        for node in start_nodes
    ])
    print(answer)


def get_cycle_length(node, instructions, network):
    cycled_instructions = itertools.cycle(instructions)

    curr = node
    n = 0
    while not curr.endswith('Z'):
        n += 1
        curr = network[curr][next(cycled_instructions)]
    cycle_length = n

    # We could just return cycle_length here. I simulate for one more cycle to
    # prove that each ghost does enter a cycle.
    expected_end = curr
    first_pass = True
    while first_pass or not curr.endswith('Z'):
        first_pass = False
        n += 1
        curr = network[curr][next(cycled_instructions)]
    assert n == cycle_length * 2
    assert curr == expected_end

    return cycle_length


if __name__ == '__main__':
    main()

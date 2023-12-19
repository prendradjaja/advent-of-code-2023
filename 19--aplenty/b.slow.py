#!/usr/bin/env python3.12
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys
import re
import itertools
from dataclasses import dataclass


def main():
    workflows, all_parts = open(sys.argv[1]).read().split('\n\n')

    all_parts = parse_parts(all_parts)
    workflows = parse_workflows(workflows)

    conditions = [
        condition
        for workflow in workflows.values()
        for condition, jump_target in workflow
        if not isinstance(condition, AlwaysPass)
    ]

    ranges = {
        var_name: get_ranges(conditions, var_name)
        for var_name in 'xmas'
    }

    answer = 0
    expected_iterations = len(ranges['x']) * len(ranges['m']) * len(ranges['a']) * len(ranges['s'])
    n = 0
    for x in ranges['x']:
        for m in ranges['m']:
            for a in ranges['a']:
                for s in ranges['s']:
                    part = {
                        'x': x[0],
                        'm': m[0],
                        'a': a[0],
                        's': s[0],
                    }
                    if 'A' == categorize_part(workflows, part):
                        group_size = len(x) * len(m) * len(a) * len(s)
                        answer += group_size
                    n += 1
                    if n % 100_000 == 0:
                        print(f'Working... completed {n:,} of {expected_iterations:,} iterations ({n / expected_iterations:.5%})')

    # Estimated runtime: 44 hours
    print(answer)


def get_ranges(conditions, var_name):
    edges = sorted({1, 4000} | {
        each.value
        for each in conditions
        if each.var_name == var_name
    })
    ranges = [
        range(1, 1+1)
    ]
    for a, b in itertools.pairwise(edges):
        my_range = range(a + 1, b)
        if my_range:
            ranges.append(my_range)
        ranges.append(range(b, b+1))
    return ranges


def categorize_part(workflows, part):
    name = 'in'
    while name not in ['A', 'R']:
        workflow = workflows[name]
        name = run_workflow(workflow, part)
    return name


def run_workflow(workflow, part):
    for condition, jump_target in workflow:
        if condition(part):
            return jump_target
    raise Exception('unreachable case')


def parse_parts(text):
    result = []
    for line in text.splitlines():
        line = re.sub(r'[^0-9]', ' ', line)
        part = {ch: int(n) for ch, n in zip('xmas', line.split())}
        result.append(part)
    return result


def parse_workflows(text):
    def parse_workflow(line):
        name, rest = line.split('{')
        assert rest.endswith('}')
        rules = rest[:-1].split(',')
        return name, [parse_rule(each) for each in rules]

    def parse_rule(rule):
        if ':' not in rule:
            return (AlwaysPass(), rule)
        else:
            condition_text, destination = rule.split(':')
            ch, op, *n = condition_text
            n = int(''.join(n))
            condition = Condition(ch, op, n)
            return (condition, destination)

    result = {}
    for line in text.splitlines():
        name, rules = parse_workflow(line)
        result[name] = rules
    return result


class AlwaysPass:
    def __call__(self, workflow):
        return True


@dataclass
class Condition:
    '''
    An introspectable function that always has the structure `VAR < VALUE` or
    `VAR > VALUE`
    '''

    var_name: ...
    operator: ...
    value: ...

    def __post_init__(self):
        assert self.var_name in 'xmas'
        assert self.operator in '<>'

    def __call__(self, workflow):
        if self.operator == '>':
            return workflow[self.var_name] > self.value
        elif self.operator == '<':
            return workflow[self.var_name] < self.value
        raise Exception('unreachable case')


if __name__ == '__main__':
    main()

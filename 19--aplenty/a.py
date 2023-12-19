#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
'''

import sys
import re


def main():
    workflows, all_parts = open(sys.argv[1]).read().split('\n\n')

    all_parts = parse_parts(all_parts)
    workflows = parse_workflows(workflows)

    accepted = [
        part
        for part in all_parts
        if 'A' == categorize_part(workflows, part)
    ]

    answer = sum(
        sum(part.values())
        for part in accepted
    )
    print(answer)


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
            return (lambda workflow: True, rule)
        else:
            condition_text, destination = rule.split(':')
            ch, op, *n = condition_text
            n = int(''.join(n))
            assert ch in 'xmas'
            assert op in '<>'
            if op == '>':
                condition = lambda workflow: workflow[ch] > n
            elif op == '<':
                condition = lambda workflow: workflow[ch] < n
            else:
                raise Exception('unreachable case')
            return (condition, destination)

    result = {}
    for line in text.splitlines():
        name, rules = parse_workflow(line)
        result[name] = rules
    return result


if __name__ == '__main__':
    main()

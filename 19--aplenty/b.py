#!/usr/bin/env python3.12

# Usage:
#     ./b.py PATH_TO_INPUT_FILE
#     ./b.py PATH_TO_INPUT_FILE -t
#         # To display the tree
#
# Explanation:
#
# It would take too long to try all 256,000,000,000,000 possible parts.
#
# Another idea comes to mind readily from an earlier puzzle this year (day 5).
# Can we use a similar trick, i.e., consider a small set of "interesting
# values" to partition the space and try a smaller number of parts? This would
# reduce the runtime by multiple orders of magnitude, but it would still take
# quite a long time: see b.slow.py.
#
# Instead, we can consider the decision tree of possible cases. To illustrate,
# consider tiny_example.txt, consisting of these workflows:
#
#     in{x>10:bigx,smallx}
#     bigx{m>10:R,A}
#     smallx{m>10:A,R}
#
# This workflow accepts a part if and only if "x is big XOR m is big". We can
# draw the decision tree like this:
#
#                 ---------
#                | x > 10? |
#                 ---------
#             /               \
#           YES               NO
#           /                   \
#       ---------           ---------
#      | m > 10? |         | m > 10? |
#       ---------           ---------
#         /   \               /   \
#       YES    NO           YES    NO
#       /       \           /       \
#    ------   ------     ------   ------
#   |Accept| |Reject|   |Accept| |Reject|
#    ------   ------     ------   ------
#
# We can create a similar decision tree for the puzzle input. It's much larger
# than this one, of course, but it's a manageable size and we can use a
# traversal to solve the problem.
#
# (We can tell before trying this approach that the tree will be a manageable
# size by counting the number of commas in the workflows. This gives an
# approximation of the number of edges in the tree. In my puzzle input, there
# are about one thousand commas in the workflows.)

import sys
import re
import itertools
from dataclasses import dataclass
import math


def main():
    workflows, all_parts = open(sys.argv[1]).read().split('\n\n')
    show_tree = '-t' in sys.argv

    all_parts = parse_parts(all_parts)
    workflows = parse_workflows(workflows)

    root = make_tree(workflows, 'in', 0)

    if show_tree:
        print(root)

    answer = 0
    for *path, result in traverse_tree(root, []):
        if result == 'R':
            continue
        assert result == 'A'

        groups = {ch: set(range(1, 4001)) for ch in 'xmas'}
        for condition in path:
            var_name = condition.var_name
            groups[var_name] &= {n for n in range(1, 4001) if condition({ var_name: n })}

        answer += math.prod(len(g) for g in groups.values())

    print(answer)


def make_tree(workflows, name, step):
    if name in ['A', 'R']:
        assert step == 0
        return TreeNode(name)

    condition, jump_target = workflows[name][step]
    if isinstance(condition, AlwaysPass):
        return make_tree(workflows, jump_target, 0)
    else:
        return TreeNode(
            condition,
            [
                make_tree(workflows, jump_target, 0),
                make_tree(workflows, name, step + 1),
            ]
        )


def traverse_tree(tree_node, path):
    if not tree_node.children:
        yield path + [tree_node.value]
    else:
        for i, child in enumerate(tree_node.children):
            assert isinstance(tree_node.value, Condition)
            if i == 0:
                condition = tree_node.value
            elif i == 1:
                condition = tree_node.value.invert()
            else:
                raise Exception('unreachable case')
            yield from traverse_tree(child, path + [condition])


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

    def __repr__(self):
        return 'AlwaysPass()'


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
        assert self.operator in ['<', '>', '<=', '>=']

    def __call__(self, workflow):
        if self.operator == '>':
            return workflow[self.var_name] > self.value
        elif self.operator == '<':
            return workflow[self.var_name] < self.value
        elif self.operator == '>=':
            return workflow[self.var_name] >= self.value
        elif self.operator == '<=':
            return workflow[self.var_name] <= self.value
        raise Exception('unreachable case')

    def invert(self):
        new_operator = {
            '>': '<=',
            '<': '>=',
            '>=': '<',
            '<=': '>',
        }[self.operator]
        return Condition(self.var_name, new_operator, self.value)

    def __repr__(self):
        return f'{self.var_name} {self.operator} {self.value}'


# Might be simpler to use a binary tree data structure specifically
class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        if children is None:
            self.children = []
        else:
            self.children = children

    def __str__(self):
        return self._to_string()

    def _to_string(self, depth=0):
        indent = '  ' * depth
        self_string = indent + str(self.value)
        children_string = ''
        for child in self.children:
            children_string += '\n' + child._to_string(depth + 1)
        return self_string + children_string


if __name__ == '__main__':
    main()

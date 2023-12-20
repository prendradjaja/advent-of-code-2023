#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys
from dataclasses import dataclass
from collections import deque, Counter


LOW = 'low'
HIGH = 'high'

BUTTON = 'button'
BROADCASTER = 'broadcaster'


def main():
    modules = {}
    for line in open(sys.argv[1]).read().splitlines():
        identifier, destinations_text = line.split(' -> ')
        if identifier == BROADCASTER:
            clazz = Broadcast
            name = identifier
        elif identifier.startswith('%'):
            clazz = FlipFlop
            name = identifier[1:]
        elif identifier.startswith('&'):
            clazz = Conjunction
            name = identifier[1:]
        else:
            raise Exception('unreachable case')
        modules[name] = clazz(name, destinations_text.split(', '))

    for source_name, source in modules.items():
        for destination_name in source.destination_names:
            destination = modules.get(destination_name)
            if isinstance(destination, Conjunction):
                destination.add_input(source_name)

    counts = Counter()
    for _ in range(1000):
        counts += press_button(modules)

    answer = counts[LOW] * counts[HIGH]
    print(answer)


def press_button(modules):
    queue = deque([Pulse(BUTTON, BROADCASTER, LOW)])
    counts = Counter()
    while queue:
        pulse = queue.popleft()
        counts[pulse.type] += 1
        if pulse.destination_name in modules:
            module = modules[pulse.destination_name]
            queue.extend(module.handle_pulse(pulse))
    return counts


def other(pulse_type):
    return {
        LOW: HIGH,
        HIGH: LOW,
    }[pulse_type]


@dataclass
class Pulse:
    source_name: ...
    destination_name: ...
    type: ...

    def __repr__(self):
        return f'{self.source_name} -{self.type}-> {self.destination_name}'


@dataclass
class Broadcast:
    name: ...
    destination_names: ...

    def handle_pulse(self, pulse):
        # This list comprehension is used in each module type, with only the
        # pulse type differing. Can be DRYed.
        return [
            Pulse(self.name, each, pulse.type)
            for each in self.destination_names
        ]


@dataclass
class FlipFlop:
    name: ...
    destination_names: ...

    def __post_init__(self):
        self.is_on = False

    def handle_pulse(self, pulse):
        if pulse.type == LOW:
            self.is_on = not self.is_on
            output_type = {
                True: HIGH,
                False: LOW,
            }[self.is_on]
            return [
                Pulse(self.name, each, output_type)
                for each in self.destination_names
            ]
        else:
            return []


@dataclass
class Conjunction:
    name: ...
    destination_names: ...

    def __post_init__(self):
        self.memory = {}

    def add_input(self, name):
        self.memory[name] = LOW

    def handle_pulse(self, pulse):
        self.memory[pulse.source_name] = pulse.type
        all_high = all(each == HIGH for each in self.memory.values())
        output_type = {
            True: LOW,
            False: HIGH,
        }[all_high]
        return [
            Pulse(self.name, each, output_type)
            for each in self.destination_names
        ]


if __name__ == '__main__':
    main()

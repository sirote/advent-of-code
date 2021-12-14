"""Day 14: Extended Polymerization"""


import os
from collections import Counter, defaultdict
from itertools import tee


INPUT = os.path.join(os.path.dirname(__file__), 'input')


class ExtendedPolymerization:

    def __init__(self, template, insertions):
        self.insertions = dict(insertions)
        self._template = template
        self._counts = Counter(self._pairwise(template))
        self._iterator = iter(self)

    def __iter__(self):
        while True:
            temp = defaultdict(int)
            for pair, count in self._counts.items():
                element = self.insertions[''.join(pair)]
                temp[pair[0], element] += count
                temp[element, pair[1]] += count

            self._counts = temp
            yield self

    def __next__(self):
        return next(self._iterator)

    @property
    def most_common(self):
        element_to_count = self._count()
        return max(element_to_count.items(), key=lambda x: x[1])

    @property
    def least_common(self):
        element_to_count = self._count()
        return min(element_to_count.items(), key=lambda x: x[1])

    def _count(self):
        element_to_count = Counter()
        for pair, count in self._counts.items():
            element_to_count[pair[0]] += count
        element_to_count[self._template[-1]] += 1
        return element_to_count

    @staticmethod
    def _pairwise(iterable):
        first, second = tee(iterable)
        next(second, None)
        return zip(first, second)


def parse(filename):
    with open(filename, encoding='utf-8') as input_file:
        template = next(input_file).strip()
        insertions = [
            tuple(s.strip() for s in line.split('->'))
            for line in input_file
            if line.strip()
        ]
        return template, insertions


def test_part1():
    assert _diff(10) == 4517


def test_part2():
    assert _diff(40) == 4704817645083


def _diff(steps):
    polymer = ExtendedPolymerization(*parse(INPUT))
    for _ in range(steps):
        next(polymer)

    return polymer.most_common[1] - polymer.least_common[1]

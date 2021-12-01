"""Day 1: Sonar Sweep"""


import os
from itertools import tee


INPUT = os.path.join(os.path.dirname(__file__), 'input')


class SonarSweep:

    def __init__(self, input_file):
        self.input_file = input_file

    def count_depth_increases(self, window=1):
        """Count the number of times a depth measurement increases from
        the previous measurement.
        """
        return sum(
            depth2 > depth1
            for depth1, depth2 in _tuples(self._iter_depths(window))
        )

    def _iter_depths(self, window):
        return (sum(depths) for depths in _tuples(self._iter_data(), n=window))

    def _iter_data(self):
        with open(self.input_file, encoding='utf-8') as input_file:
            for line in input_file:
                yield int(line)


def _tuples(iterable, n=2):
    iterators = tee(iterable, n)
    for i in range(1, n):
        for iterator in iterators[i:]:
            next(iterator, None)
    return zip(*iterators)


def test_part1():
    assert SonarSweep(INPUT).count_depth_increases() == 1709


def test_part2():
    assert SonarSweep(INPUT).count_depth_increases(window=3) == 1761

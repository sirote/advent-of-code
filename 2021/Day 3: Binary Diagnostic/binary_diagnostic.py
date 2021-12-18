"""Day 3: Binary Diagnostic."""


import os
from functools import cached_property
from itertools import count
from pathlib import Path


PATH = Path(__file__).parent


class BinaryDiagnostic:

    def __init__(self, path):
        self.path = path

    @property
    def power_consumption(self):
        return self._get_gamma_rate() * self._get_epsilon_rate()

    @property
    def life_support_rating(self):
        return (
            self._get_oxygen_generator_rating()
            * self._get_co2_scrubber_rating()
        )

    def _get_gamma_rate(self):
        return int(self._rate, 2)

    def _get_epsilon_rate(self):
        binary = self._rate.translate(str.maketrans('01', '10'))
        return int(binary, 2)

    @cached_property
    def _rate(self):
        lines = self._iter_lines()
        counts = [int(char) for char in next(lines)]
        total = 1

        for line in lines:
            total += 1
            for index, char in enumerate(line):
                counts[index] += int(char)

        return ''.join('1' if count > total // 2 else '0' for count in counts)

    def _get_oxygen_generator_rating(self):
        return self._get_rating(lambda g0, g1: len(g0) > len(g1))

    def _get_co2_scrubber_rating(self):
        return self._get_rating(lambda g0, g1: len(g0) <= len(g1))

    def _get_rating(self, criteria):
        lines =  self._iter_lines()
        for index in count():
            bit_groups = {'0': [], '1': []}
            for line in lines:
                bit_groups[line[index]].append(line)

            if criteria(group0 := bit_groups['0'], group1 := bit_groups['1']):
                lines = group0
            else:
                lines = group1

            if len(lines) == 1:
                break

        return int(lines[0], 2)

    def _iter_lines(self):
        with self.path.open(encoding='utf-8') as input_file:
            for line in input_file:
                yield line.rstrip()


def test_part1():
    assert BinaryDiagnostic(PATH / 'input').power_consumption == 3923414


def test_part2():
    assert BinaryDiagnostic(PATH / 'input').life_support_rating == 5852595

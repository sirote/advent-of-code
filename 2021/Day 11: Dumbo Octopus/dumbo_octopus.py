"""Day 11: Dumbo Octopus"""


import os
from itertools import count


INPUT = os.path.join(os.path.dirname(__file__), 'input')


class DumboOctopuses:

    def __init__(self, octopuses):
        self.flashes = 0
        self._octopuses = octopuses
        self._row_max = len(octopuses)
        self._col_max = len(octopuses[0])
        self._iterator = iter(self)

    def __str__(self):
        return '\n'.join(
            ''.join(
                str(octopus) if octopus else '\033[1m0\033[0m'
                for octopus in row
            )
            for row in self._octopuses
        )

    def __iter__(self):
        for _ in count():
            flashed = set()
            for row in range(self._row_max):
                for col in range(self._col_max):
                    self._increase(row, col, flashed)
            yield self

    def __next__(self):
        return next(self._iterator)

    @property
    def synchronized(self):
        return all(level == 0 for row in self._octopuses for level in row)

    def _increase(self, row, col, flashed):
        if (row, col) in flashed:
            return

        if (level := self._octopuses[row][col] + 1) > 9:
            self._flash(row, col)
            flashed.add((row, col))
            for adj_row, adj_col in self._adjacents(row, col):
                self._increase(adj_row, adj_col, flashed)
        else:
            self._octopuses[row][col] = level

    def _flash(self, row, col):
        self._octopuses[row][col] = 0
        self.flashes += 1

    def _adjacents(self, row, col):
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 and j == 0:
                    continue

                adj_row = row + i
                adj_col = col + j

                if (0 <= adj_row < self._row_max
                        and 0 <= adj_col < self._col_max):
                    yield adj_row, adj_col


def parse(filename):
    with open(filename, encoding='utf-8') as input_file:
        return [
            [int(number) for number in line.strip()]
            for line in input_file
        ]


def test_part1():
    octopuses = DumboOctopuses(parse(INPUT))
    for _ in range(100):
        next(octopuses)

    assert octopuses.flashes == 1652


def test_part2():
    octopuses = DumboOctopuses(parse(INPUT))
    step = 0
    for step in count(start=1):
        if next(octopuses).synchronized:
            break

    assert step == 220

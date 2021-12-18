"""Day 9: Smoke Basin"""


import operator
from functools import reduce
from itertools import chain
from pathlib import Path


PATH = Path(__file__).parent

HIGHEST = '9'


class SmokeBasin:

    def __init__(self, path):
        self.heightmap = list(self._parse(path))

    @property
    def low_point_heights(self):
        """A list of heights of all low points."""
        return [
            int(self.heightmap[i][j])
            for i, j in self._locations()
            if self._lowest(i, j)
        ]

    @property
    def sizes(self):
        """A list of all basin sizes."""
        basin_sizes = []
        visited = set()

        for i, j in filter(lambda l: l not in visited, self._locations()):
            size = 0
            locations = [(i, j)]

            while locations:
                location = locations.pop()
                if location in visited:
                    continue

                visited.add(location)
                row, col = location
                if self.heightmap[row][col] == HIGHEST:
                    continue

                size += 1
                locations.extend(self._adjacents(row, col))

            basin_sizes.append(size)

        return basin_sizes

    def _lowest(self, row, col):
        return self.heightmap[row][col] < min(
            self.heightmap[i][j]
            for i, j in self._adjacents(row, col)
        )

    def _locations(self):
        for i in range(1, len(self.heightmap) - 1):
            for j in range(1, len(self.heightmap[0]) - 1):
                yield i, j

    @staticmethod
    def _adjacents(row, col):
        for i, j in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yield row + i, col + j

    @staticmethod
    def _parse(filename):
        with open(filename, encoding='utf-8') as input_file:
            line = next(input_file, '').strip()
            padded = HIGHEST * (len(line) + 2)
            yield padded

            for line in chain((line,), input_file):
                yield f'{HIGHEST}{line.strip()}{HIGHEST}'

            yield padded


def test_part1():
    smoke_basin = SmokeBasin(PATH / 'input')
    risk_levels = [height + 1 for height in smoke_basin.low_point_heights]
    assert sum(risk_levels) == 462


def test_part2():
    smoke_basin = SmokeBasin(PATH / 'input')
    assert reduce(operator.mul, sorted(smoke_basin.sizes)[-3:], 1) == 1397760

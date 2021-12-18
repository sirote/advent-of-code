"""Day 15: Chiton"""


import math
from heapq import heappush, heappop
from pathlib import Path


PATH = Path(__file__).parent


class RiskMap:

    def __init__(self, data, factor=None):
        self.data = self._enlarge(data, factor) if factor else data

    def __iter__(self):
        return self.data.__iter__()

    def __getitem__(self, key):
        src, dst = key
        if dst in self.adjacents(src):
            return self.data[dst[0]][dst[1]]
        return math.inf

    @property
    def dimensions(self):
        return len(self.data), len(self.data[0])

    def adjacents(self, coordinate):
        i, j = coordinate
        max_i, max_j = self.dimensions
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < max_i and 0 <= y < max_j:
                yield x, y

    @classmethod
    def _enlarge(cls, data, factor):
        rows = len(data)
        cols = len(data[0])
        new_data = [
            [0] * cols * factor
            for _ in range(rows * factor)
        ]
        for i in range(len(new_data)):
            for j in range(len(new_data[i])):
                inc_row = i // rows
                inc_col = j // cols
                level = data[i % rows][j % cols] + inc_row + inc_col
                new_data[i][j] = 1 + (level - 1) % 9

        return new_data


class Cavern:

    def __init__(self, cavern):
        self.cavern = cavern
        self._predecessor = {}
        self._end = None

    def __str__(self):
        paths = set()
        coord = self._end
        while coord:
            paths.add(coord)
            coord = self._predecessor.get(coord)

        return '\n'.join(
            ''.join(
                f'\033[95m{risk_level}\033[0m'
                if (i, j) in paths else str(risk_level)
                for j, risk_level in enumerate(row)
            )
            for i, row in enumerate(self.cavern)
        )

    def find_lowest_risk(self, start, end=None):
        self._end = end or tuple(d - 1 for d in self.cavern.dimensions)
        self._predecessor = {}
        graph = self.cavern
        distances = {start: 0}
        queue = [(0, start)]
        visited = set()

        while queue:
            _, src = heappop(queue)
            if src == self._end:
                break

            if src in visited:
                continue

            visited.add(src)
            for dst in graph.adjacents(src):
                distance = self._set_distances(src, dst, distances)
                heappush(queue, (distance, dst))

        return distances[self._end]

    def _set_distances(self, src, dst, distances):
        dist = distances.get(src, math.inf) + self.cavern[src, dst]
        if dist < distances.get(dst, math.inf):
            distances[dst] = dist
            self._predecessor[dst] = src

        return dist


def parse(path):
    with path.open(encoding='utf-8') as input_file:
        return [
            [int(n) for n in line.strip()]
            for line in input_file
        ]


def test_part1():
    risk_map = RiskMap(parse(PATH / 'input'))
    cavern = Cavern(risk_map)
    risk_level = cavern.find_lowest_risk(start=(0, 0))
    print()
    print(cavern)
    assert risk_level == 361


def test_part2():
    risk_map = RiskMap(parse(PATH / 'input'), factor=5)
    assert Cavern(risk_map).find_lowest_risk(start=(0, 0)) == 2838

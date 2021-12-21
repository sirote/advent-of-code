"""Day 20: Trench Map"""


import math
from itertools import product
from pathlib import Path


PATH = Path(__file__).parent

LIGHT = '#'
DARK = '.'


class TrenchMap:

    def __init__(self, enhancement, image):
        self._enhancement = enhancement
        self._image = image
        self._iterations = 0
        self._iterator = iter(self)

    def __str__(self):
        min_row, min_col, max_row, max_col = self._boundary
        return '\n'.join(
            ''.join(
                LIGHT if (i, j) in self._image else DARK
                for j in range(min_row, max_row + 1)
            )
            for i in range(min_col, max_col + 1)
        )

    def __len__(self):
        if self._infinite_light:
            return math.inf
        return len(self._image)

    def __iter__(self):
        while True:
            min_row, min_col, max_row, max_col = self._boundary
            enhanced_image = set()

            if self._infinite_light:
                for i in range(min_row - 2, max_row + 3):
                    for k in (1, 2):
                        self._image.add((i, min_col - k))
                        self._image.add((i, max_col + k))

                for j in range(min_col - 2, max_col + 3):
                    for k in (1, 2):
                        self._image.add((min_row - k, j))
                        self._image.add((max_row + k, j))

            for i in range(min_row - 1, max_row + 2):
                for j in range(min_col - 1, max_col + 2):
                    index = self._get_index(i, j)
                    if self._enhancement[index] == LIGHT:
                        enhanced_image.add((i, j))

            self._image = enhanced_image
            self._iterations += 1
            yield self

    def __next__(self):
        return next(self._iterator)

    def _get_index(self, pixel_x, pixel_y):
        binary_number = ''.join(
            '1' if (pixel_x + i, pixel_y + j) in self._image else '0'
            for i, j in product((-1, 0, 1), repeat=2)
        )
        return int(binary_number, 2)

    @property
    def _boundary(self):
        min_row = min_col = math.inf
        max_row = max_col = -math.inf
        for i, j in self._image:
            min_row = min(min_row, i)
            min_col = min(min_col, j)
            max_row = max(max_row, i)
            max_col = max(max_col, j)

        return min_row, min_col, max_row, max_col

    @property
    def _infinite_light(self):
        return (
            self._enhancement[0] == LIGHT
            and (self._enhancement[-1] == LIGHT or self._iterations % 2 == 1)
        )


def parse(path):
    with path.open(encoding='utf-8') as input_file:
        enhancement = next(input_file).strip()
        rows = [row for line in input_file if (row := line.strip())]
        image = {
            (i, j)
            for i, row in enumerate(rows)
            for j, pixel in enumerate(row)
            if pixel == LIGHT
        }
        return enhancement, image


def test_example1():
    trench_map = TrenchMap(*parse(PATH / 'example'))
    for _ in range(2):
        next(trench_map)
        print()
        print(trench_map)

    assert len(trench_map) == 35


def test_example2():
    trench_map = TrenchMap(*parse(PATH / 'example'))
    for _ in range(50):
        next(trench_map)

    assert len(trench_map) == 3351


def test_part1():
    trench_map = TrenchMap(*parse(PATH / 'input'))
    for _ in range(2):
        next(trench_map)

    assert len(trench_map) == 5301


def test_part2():
    trench_map = TrenchMap(*parse(PATH / 'input'))
    for _ in range(50):
        next(trench_map)

    assert len(trench_map) == 19492

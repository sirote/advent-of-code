"""Day 5: Hydrothermal Venture"""


import os
from collections import Counter
from itertools import repeat
from typing import NamedTuple


INPUT = os.path.join(os.path.dirname(__file__), 'input')


def parse(filename):
    with open(filename, encoding='utf-8') as input_file:
        for line in input_file:
            start, end = line.split('->')
            yield (_parse_point(start), _parse_point(end))


def _parse_point(point):
    x, y = point.split(',')
    return Point(int(x), int(y))


class Point(NamedTuple):

    x: int
    y: int


class Diagram1:

    def __init__(self):
        self.diagram = Counter()

    def __str__(self):
        size = max(max(self.diagram)) + 1
        return '\n'.join(
            ''.join(
                str(self.diagram.get((j, i), '.'))
                for j in range(size)
            )
            for i in range(size)
        )

    @property
    def overlap_points(self):
        return sum(value > 1 for value in self.diagram.values())

    def draw(self, data):
        for start, end in data:
            if start.x == end.x or start.y == end.y:
                self._draw(start, end)

    def _draw(self, start, end):
        dx = end.x - start.x
        dy = end.y - start.y

        if dx == 0:
            step = 1 if start.y < end.y else -1
            xs = repeat(start.x)
            ys = range(start.y, end.y + step, step)
        elif dy == 0:
            step = 1 if start.x < end.x else -1
            xs = range(start.x, end.x + step, step)
            ys = repeat(start.y)
        else:
            if abs(dx) > abs(dy):
                step_x = dx // abs(dy)
                step_y = dy // abs(dy)
            else:
                step_x = dx // abs(dx)
                step_y = dy // abs(dx)

            xs = range(start.x, end.x + (1 if dx > 0 else -1), step_x)
            ys = range(start.y, end.y + (1 if dy > 0 else -1), step_y)

        for x, y in zip(xs, ys):
            self.diagram[x, y] += 1


class Diagram2(Diagram1):

    def draw(self, data):
        for start, end in data:
            self._draw(start, end)


def test_part1():
    diagram = Diagram1()
    diagram.draw(parse(INPUT))
    assert diagram.overlap_points == 7142


def test_part2():
    diagram = Diagram2()
    diagram.draw(parse(INPUT))
    assert diagram.overlap_points == 20012

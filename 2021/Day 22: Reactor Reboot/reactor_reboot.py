"""Day 22: Reactor Reboot"""


import operator
from functools import reduce
from pathlib import Path


PATH = Path(__file__).parent


X = 0
Y = 1
Z = 2


class ReactorReboot:

    def __init__(self):
        self.cuboids = []

    @property
    def cubes_on(self):
        """Number of cubes that are on."""
        return sum(cuboid.volume for cuboid in self.cuboids)

    def process(self, step):
        is_on, cuboid = step
        if is_on:
            self.turn_on(cuboid)
        else:
            self.turn_off(cuboid)

    def turn_on(self, cuboid):
        if not self.cuboids:
            self.cuboids.append(cuboid)
            return

        self.cuboids.extend(self._intersections(cuboid))
        self.cuboids.append(cuboid)

    def turn_off(self, cuboid):
        if not self.cuboids:
            return

        self.cuboids.extend(self._intersections(cuboid))

    def _intersections(self, cuboid):
        return [
            -intersect
            for _cuboid in self.cuboids
            if (intersect := _cuboid & cuboid)
        ]


class Cuboid:

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.negative = False

    def __repr__(self):
        sign = '-' if self.negative else ''
        return f'{sign}Cuboid({self.point1}, {self.point2})'

    def __neg__(self):
        cuboid = Cuboid(self.point1, self.point2)
        cuboid.negative = not self.negative
        return cuboid

    def __and__(self, other):
        if not self.overlaps(other):
            return None

        point1 = (
            max(self.point1[X], other.point1[X]),
            max(self.point1[Y], other.point1[Y]),
            max(self.point1[Z], other.point1[Z]),
        )
        point2 = (
            min(self.point2[X], other.point2[X]),
            min(self.point2[Y], other.point2[Y]),
            min(self.point2[Z], other.point2[Z]),
        )
        if self.negative != other.negative:
            return -Cuboid(point1, point2)
        return Cuboid(point1, point2)

    @property
    def volume(self):
        return reduce(operator.mul, (
            abs(a - b) + 1
            for a, b in zip(self.point1, self.point2)
        )) * (-1 if self.negative else 1)

    def overlaps(self, other):
        return (
            self.point1[X] <= other.point2[X]
            and self.point2[X] >= other.point1[X]
            and self.point1[Y] <= other.point2[Y]
            and self.point2[Y] >= other.point1[Y]
            and self.point1[Z] <= other.point2[Z]
            and self.point2[Z] >= other.point1[Z]
        )


def parse(path):
    with path.open(encoding='utf-8') as input_file:
        steps = []
        for line in input_file:
            step = []
            if line.startswith('on'):
                step.append(True)
            elif line.startswith('off'):
                step.append(False)
            else:
                raise ValueError(f'Invalid step: {line}')

            ranges = [
                _parse_range(range_)
                for range_ in line.split(',')
            ]
            step.append(Cuboid(*zip(*ranges)))
            steps.append(step)

    return steps


def _parse_range(string):
    range_ = string.split('=')[-1]
    start, end = range_.split('..')
    return int(start), int(end)


def test_example1():
    reactor = ReactorReboot()
    for step in parse(PATH / 'example1'):
        reactor.process(step)
    assert reactor.cubes_on == 39


def test_example2():
    reactor = ReactorReboot()
    for step in parse(PATH / 'example2'):
        _, cuboid = step
        if (any(p < -50 for p in cuboid.point1)
                or any(p > 50 for p in cuboid.point2)):
            continue
        reactor.process(step)
    assert reactor.cubes_on == 590784


def test_example3():
    reactor = ReactorReboot()
    for step in parse(PATH / 'example3'):
        reactor.process(step)
    assert reactor.cubes_on == 2758514936282235


def test_part1():
    reactor = ReactorReboot()
    for step in parse(PATH / 'input'):
        _, cuboid = step
        if (any(p < -50 for p in cuboid.point1)
                or any(p > 50 for p in cuboid.point2)):
            continue
        reactor.process(step)
    assert reactor.cubes_on == 603661


def test_part2():
    reactor = ReactorReboot()
    for step in parse(PATH / 'input'):
        reactor.process(step)
    assert reactor.cubes_on == 1237264238382479

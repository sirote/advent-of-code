"""Day 7: The Treachery of Whales"""


import os


INPUT = os.path.join(os.path.dirname(__file__), 'input')


def parse(filename):
    with open(filename, encoding='utf-8') as input_file:
        return [int(position) for position in input_file.read().split(',')]


class CrabSubmarines1:

    @classmethod
    def align(cls, positions):
        """Align the crabs that costs the least fuel and return the
        amount of fuel spent.
        """
        return min(
            cls.cost(positions, position)
            for position in range(min(positions), max(positions) + 1)
        )

    @staticmethod
    def cost(positions, position):
        return sum(abs(x - position) for x in positions)


class CrabSubmarines2(CrabSubmarines1):

    @staticmethod
    def cost(positions, position):
        return sum((n := abs(x - position)) * (n + 1) // 2 for x in positions)


def test_part1():
    assert CrabSubmarines1.align(parse(INPUT)) == 347449


def test_part2():
    assert CrabSubmarines2.align(parse(INPUT)) == 98039527

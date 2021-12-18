"""Day 1: Sonar Sweep"""


from itertools import tee
from pathlib import Path


PATH = Path(__file__).parent


class SonarSweep:

    def __init__(self, path):
        self.path = path

    def count_depth_increases(self, window=1):
        """Count the number of times a depth measurement increases from
        the previous measurement.
        """
        return sum(
            depth2 > depth1
            for depth1, depth2 in _pairwise(self._iter_data(), window)
        )

    def _iter_data(self):
        with self.path.open(encoding='utf-8') as input_file:
            for line in input_file:
                yield int(line)


def _pairwise(iterable, window=1):
    first, second = tee(iterable)
    for _ in range(window):
        next(second, None)
    return zip(first, second)


def test_part1():
    assert SonarSweep(PATH / 'input').count_depth_increases() == 1709


def test_part2():
    assert SonarSweep(PATH / 'input').count_depth_increases(window=3) == 1761

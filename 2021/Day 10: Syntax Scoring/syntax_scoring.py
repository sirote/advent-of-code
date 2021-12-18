"""Day 10: Syntax Scoring"""


from collections import Counter
from functools import reduce
from pathlib import Path


PATH = Path(__file__).parent

PAIRS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}


class CorruptedSyntaxScoring:

    points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137.
    }

    def __init__(self, path):
        self.path = path

    def score(self):
        """Return the total syntax error score."""
        counts = Counter(
            char
            for line in self._iter_lines()
            if (char := self._process(line))
        )
        return sum(
            self.points[char] * count
            for char, count in counts.items()
        )

    @staticmethod
    def _process(line):
        stack = []
        for char in line:
            if closer := PAIRS.get(char):
                stack.append(closer)
            else:
                try:
                    if stack.pop() != char:
                        return char
                except IndexError:
                    return char

        return None

    def _iter_lines(self):
        with self.path.open(encoding='utf-8') as input_file:
            for line in input_file:
                yield line.rstrip()


class IncompleteSyntaxScoring(CorruptedSyntaxScoring):

    points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    def score(self):
        scores = [
            self._score(completion_chars)
            for line in self._iter_lines()
            if (completion_chars := self._process(line))
        ]
        return sorted(scores)[len(scores) // 2]

    def _score(self, chars):
        return reduce(lambda v, c: v * 5 + self.points[c], chars, 0)

    @staticmethod
    def _process(line):
        stack = []
        for char in line:
            if closer := PAIRS.get(char):
                stack.append(closer)
            else:
                try:
                    if stack.pop() != char:
                        break
                except IndexError:
                    break
        else:
            return reversed(stack)

        return None


def test_part1():
    assert CorruptedSyntaxScoring(PATH / 'input').score() == 374061


def test_part2():
    assert IncompleteSyntaxScoring(PATH / 'input').score() == 2116639949

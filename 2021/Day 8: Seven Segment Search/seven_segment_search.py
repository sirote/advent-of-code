"""Day 8: Seven Segment Search"""


import os
from collections import Counter, defaultdict


INPUT = os.path.join(os.path.dirname(__file__), 'input')


class Digit:
    """A seven-segment display"""

    def __init__(self, segments):
        self.segments = segments[:7]

    def __str__(self):
        def horizontal(segment):
            if segment:
                return ' #### '
            return '      '

        def vertical(segment1, segment2):
            if segment1 and segment2:
                lines = ('#    #',) * 2
            elif segment1 and not segment2:
                lines = ('#     ',) * 2
            elif not segment1 and segment2:
                lines = ('     #',) * 2
            else:
                lines = ('      ',) * 2

            return '\n'.join(lines)

        return '\n'.join((
            horizontal(self.segments[0]),
            vertical(self.segments[5], self.segments[1]),
            horizontal(self.segments[6]),
            vertical(self.segments[4], self.segments[2]),
            horizontal(self.segments[3]),
        ))

    def __repr__(self):
        return repr(self.segments)

    def __len__(self):
        return sum(self.segments)

    def __eq__(self, other):
        return self.segments == other.segments

    def __sub__(self, other):
        return sum(
            1 if segment1 and not segment2 else 0
            for segment1, segment2 in zip(self.segments, other.segments)
        )


class Digits:
    """A collection of seven-segment digits."""

    def __init__(self, digits):
        self.digits = digits

    def __str__(self):
        return '\n\n'.join(str(digit) for digit in self.digits)

    def find_indices(self, segments):
        """Return a list of indices of digits which have the same number
        of segments.
        """
        return [
            index
            for index, digit in enumerate(self.digits)
            if len(digit) == segments
        ]

    def map_indices(self, segments, patterns, known_index_to_pattern):
        """Return a dict of digit index to pattern."""
        index_to_pattern = {}
        indices = self.find_indices(segments)

        while patterns:
            for item in known_index_to_pattern.items():
                _indices = [i for i in indices if i not in index_to_pattern]
                if pairs := list(self._map_indices(_indices, patterns, *item)):
                    index_to_pattern.update(pairs)
                    _, mapped_patterns = zip(*pairs)
                    patterns = [
                        pattern
                        for pattern in patterns
                        if pattern not in mapped_patterns
                    ]
                    break
            else:
                raise RuntimeError('Unable to map indices for {patterns}')

        return index_to_pattern

    def _map_indices(self, indices, patterns, known_index, known_pattern):
        pattern_to_diff = {
            pattern: self._diff_segments(pattern, known_pattern)
            for pattern in patterns
        }
        unique_diffs = {
            diff
            for diff, count in Counter(pattern_to_diff.values()).items()
            if count == 1
        }
        for pattern, diff in pattern_to_diff.items():
            if diff not in unique_diffs:
                continue

            index = self._find_index(indices, known_index, diff)
            if index is not None:
                yield index, pattern
            else:
                raise RuntimeError(f'Unable to map indices for {patterns}')

    @staticmethod
    def _diff_segments(pattern1, pattern2):
        if len(pattern1) > len(pattern2):
            return len(pattern1 - pattern2)
        return len(pattern2 - pattern1)

    def _find_index(self, indices, index, diff):
        digit = self.digits[index]
        for i in indices:
            if self.digits[i] - digit == diff:
                return i
        return None


class Solver:
    """The puzzle solver."""

    def __init__(self, digits):
        self.digits = digits

    def solve(self, patterns, outputs):
        """Return the output value."""
        digit_to_pattern = self.identify(patterns)
        pattern_to_digit = {
            pattern: digit
            for digit, pattern in digit_to_pattern.items()
        }
        return int(''.join(
            str(pattern_to_digit[frozenset(output)])
            for output in outputs
        ))

    def identify(self, patterns):
        """Return a dict of digit index to pattern."""
        index_to_pattern = {}
        segments_to_patterns = defaultdict(list)

        for pattern in patterns:
            if not (indices := self.digits.find_indices(len(pattern))):
                raise RuntimeError(
                    f'Not found digits with {len(pattern)} segments for'
                    f' pattern {pattern}'
                )

            if len(indices) == 1:
                index_to_pattern[indices[0]] = pattern
            else:
                segments_to_patterns[len(pattern)].append(pattern)

        if not index_to_pattern:
            raise RuntimeError(f'Unable to identify patterns: {patterns}')

        for segments, _patterns in segments_to_patterns.items():
            mapped = self.digits.map_indices(
                segments, _patterns, index_to_pattern
            )
            index_to_pattern.update(mapped)

        return index_to_pattern


ZERO = Digit((True, True, True, True, True, True, False))
ONE = Digit((False, True, True, False, False, False, False))
TWO = Digit((True, True, False, True, True, False, True))
THREE = Digit((True, True, True, True, False, False, True))
FOUR = Digit((False, True, True, False, False, True, True))
FIVE = Digit((True, False, True, True, False, True, True))
SIX = Digit((True, False, True, True, True, True, True))
SEVEN = Digit((True, True, True, False, False, False, False))
EIGHT = Digit((True, True, True, True, True, True, True))
NINE = Digit((True, True, True, True, False, True, True))


def parse(filename):
    """Return an iterator of patterns/outputs pairs."""
    with open(filename, encoding='utf-8') as input_file:
        for line in input_file:
            patterns, outputs = line.split('|')
            yield _parse_patterns(patterns), outputs.strip().split()


def _parse_patterns(patterns):
    return [
        frozenset(pattern)
        for pattern in patterns.strip().split()
    ]


def test_part1():
    digits = Digits([ONE, FOUR, SEVEN, EIGHT])
    counts = sum(
        sum(bool(digits.find_indices(len(output))) for output in outputs)
        for _, outputs in parse(INPUT)
    )
    assert counts == 521


def test_part2():
    solver = Solver(Digits(
        [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]
    ))
    assert sum(solver.solve(*entry) for entry in parse(INPUT)) == 1016804

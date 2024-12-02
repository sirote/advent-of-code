"""Day 2: Red-Nosed Reports"""


from itertools import pairwise


def parse(filename):
    """Parse reports from a file, each report is a list of integers."""
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            yield [int(n) for n in line.split()]


def is_safe(report, tolerate=0, sign=0):
    """Check if the report is safe."""
    _sign = sign
    for i, (a, b) in enumerate(pairwise(report)):
        diff = a - b
        if abs(diff) > 3 or abs(diff) < 1 or diff * sign < 0:
            if tolerate < 1:
                return False

            return (
                (i == 1 and is_safe(report[1:], tolerate - 1))
                or is_safe(report[i-1:i] + report[i+1:], tolerate - 1, _sign)
                or is_safe(report[i:i+1] + report[i+2:], tolerate - 1, sign)
            )

        _sign, sign = sign, diff // abs(diff)

    return True


def test_example():
    """Test the example."""
    reports = list(parse('example.txt'))
    assert sum(is_safe(report) for report in reports) == 2
    assert sum(is_safe(report, tolerate=1) for report in reports) == 4


def test_puzzle():
    """Test the puzzle."""
    reports = list(parse('input.txt'))
    assert sum(is_safe(report) for report in reports) == 246
    assert sum(is_safe(report, tolerate=1) for report in reports) == 318

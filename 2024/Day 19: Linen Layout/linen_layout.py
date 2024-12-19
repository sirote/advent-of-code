"""Day 19: Linen Layout"""


from functools import cache


def parse(filename):
    """Parse the input file and return the available towel patterns and
    the list of desired designs.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        top, bottom = f.read().split('\n\n')
        patterns = tuple(pattern.strip() for pattern in top.split(','))
        designs = tuple(design.strip() for design in bottom.splitlines())

    return patterns, designs


def count(designs, patterns):
    """Count the number of different ways to make each design."""
    @cache
    def _count(design):
        if not design:
            return 1

        return sum(
            _count(design[len(pattern):])
            for pattern in patterns
            if design.startswith(pattern)
        )

    return {design: _count(design) for design in designs}


def test_example():
    """Test the example."""
    patterns, designs = parse('example.txt')
    counter = count(designs, patterns)
    assert len([c for c in counter.values() if c != 0]) == 6
    assert sum(counter.values()) == 16


def test_puzzle():
    """Test the puzzle."""
    patterns, designs = parse('input.txt')
    counter = count(designs, patterns)
    assert len([c for c in counter.values() if c != 0]) == 306
    assert sum(counter.values()) == 604622004681855

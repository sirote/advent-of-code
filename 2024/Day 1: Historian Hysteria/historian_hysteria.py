"""Day 1: Historian Hysteria"""


from collections import Counter


def parse(filename):
    """Parse the input file and return two lists of integers."""
    with open(filename, 'r', encoding='utf-8') as f:
        numbers = [int(n) for line in f for n in line.split()]
    return numbers[::2], numbers[1::2]


def total_distance(l1, l2):
    """Return the total distance between two lists of integers."""
    return sum(abs(a - b) for a, b in zip(sorted(l1), sorted(l2)))


def similarity_score(l1, l2):
    """Return the similarity score between two lists of integers."""
    counter = Counter(l2)
    return sum(counter[n] * n for n in l1)


def test_example():
    """Test the example."""
    l1, l2 = parse('example.txt')
    assert total_distance(l1, l2) == 11
    assert similarity_score(l1, l2) == 31


def test_puzzle():
    """Test the puzzle."""
    l1, l2 = parse('input.txt')
    assert total_distance(l1, l2) == 1530215
    assert similarity_score(l1, l2) == 26800609

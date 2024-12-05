"""Day 5: Print Queue"""


from collections import defaultdict
from functools import cmp_to_key
from itertools import takewhile


def parse(filename):
    """Return the page ordering rules and the lists of updates
    containing the page numbers.
    """
    rules = defaultdict(set)
    with open(filename, 'r', encoding='utf-8') as f:
        for line in takewhile(lambda x: x.strip(), f):
            page1, page2 = line.strip().split('|')
            rules[page1].add(page2)

        updates = [line.strip().split(',') for line in f]

    return rules, updates


def ordered(update, rules):
    """Return the ordered list of pages after applying the rules."""
    def cmp(a, b):
        if b in rules[a]:
            return -1
        return 1
    return sorted(update, key=cmp_to_key(cmp))


def test_example():
    """Test the example."""
    rules, updates = parse('example.txt')
    ordered_updates = [ordered(update, rules) for update in updates]
    assert sum(
        int(u[len(u) // 2])
        for u, ou in zip(updates, ordered_updates)
        if u == ou
    ) == 143
    assert sum(
        int(ou[len(ou) // 2])
        for u, ou in zip(updates, ordered_updates)
        if u != ou
    ) == 123


def test_puzzle():
    """Test the puzzle."""
    rules, updates = parse('input.txt')
    ordered_updates = [ordered(update, rules) for update in updates]
    assert sum(
        int(u[len(u) // 2])
        for u, ou in zip(updates, ordered_updates)
        if u == ou
    ) == 6949
    assert sum(
        int(ou[len(ou) // 2])
        for u, ou in zip(updates, ordered_updates)
        if u != ou
    ) == 4145

"""Day 13: Distress Signal"""


from ast import literal_eval
from functools import cmp_to_key
from itertools import chain, takewhile, zip_longest


def parse(filename):
    """Return an interable of pairs of packets."""
    with open(filename, 'r', encoding='utf-8') as file_:
        while pair := _parse(takewhile(lambda line: line.rstrip(), file_)):
            yield pair


def _parse(lines):
    try:
        left, right = [line.rstrip() for line in lines]
    except ValueError:
        return None
    return literal_eval(left), literal_eval(right)


def compare(left, right):
    """Return -1 for less-than, 0 if the inputs are equal, or 1 for
    greater-than.
    """
    for i, j in zip_longest(left, right):
        if i is None:
            return -1

        if j is None:
            return 1

        if isinstance(i, list) and isinstance(j, list):
            if result := compare(i, j):
                return result
            continue

        if isinstance(i, list):
            if result := compare(i, [j]):
                return result
            continue

        if isinstance(j, list):
            if result := compare([i], j):
                return result
            continue

        if i == j:
            continue

        return -1 if i < j else 1

    return 0


def main():
    """Main entry."""
    pairs = list(parse('input'))
    assert sum(
        index
        for index, pair in enumerate(pairs, start=1)
        if compare(*pair) == -1
    ) == 4809

    two, six = [[2]], [[6]]
    packets = sorted(chain((two, six), *pairs), key=cmp_to_key(compare))
    assert (packets.index(two) + 1) * (packets.index(six) + 1) == 22600


if __name__ == '__main__':
    main()

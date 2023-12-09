"""Day 9: Mirage Maintenance"""


from itertools import pairwise


def parse(filename):
    """Parse a list of values from the environmental report."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            yield [int(value) for value in line.strip().split()]


def extrapolate_forward(history):
    """Extrapolate the next value in the history."""
    return sum(
        diffs[-1]
        for diffs in iter_differences(history)
    )


def extrapolate_backward(history):
    """Extrapolate the previous value in the history."""
    return sum(
        diffs[0] * (-1) ** n
        for n, diffs in enumerate(iter_differences(history))
    )


def iter_differences(history):
    """Iterate over the sequence of differences in the history."""
    while any(v != 0 for v in history):
        yield history
        history = [b - a for a, b in pairwise(history)]


def main():
    """Main program."""
    histories = list(parse('input'))
    assert sum(
        extrapolate_forward(history)
        for history in histories
    ) == 1584748274
    assert sum(
        extrapolate_backward(history)
        for history in histories
    ) == 1026


if __name__ == '__main__':
    main()

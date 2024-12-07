"""Day 7: Bridge Repair"""


OPERATORS = {
    '+': lambda x, y: x + y,
    '*': lambda x, y: x * y,
    '||': lambda x, y: int(f'{x}{y}'),
}


def parse(filename):
    """Parse the input file and return a generator of test values and
    numbers.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            test_value, _, numbers = line.partition(':')
            yield int(test_value), [int(n) for n in numbers.split()]


def check(test_value, numbers, operators=()):
    """Check if the given numbers can be combined to get the test
    value.
    """
    queue = [(1, numbers[0])]
    while queue:
        i, x = queue.pop()
        try:
            y = numbers[i]
        except IndexError:
            if x == test_value:
                return True
        else:
            queue.extend((i + 1, OPERATORS[op](x, y)) for op in operators)

    return False


def test_example():
    """Test the example."""
    equations = list(parse('example.txt'))
    assert sum(
        test_value
        for test_value, numbers in equations
        if check(test_value, numbers, operators=('+', '*'))
    ) == 3749
    assert sum(
        test_value
        for test_value, numbers in equations
        if check(test_value, numbers, operators=('+', '*', '||'))
    ) == 11387


def test_puzzle():
    """Test the puzzle."""
    equations = list(parse('input.txt'))
    assert sum(
        test_value
        for test_value, numbers in equations
        if check(test_value, numbers, operators=('+', '*'))
    ) == 882304362421
    assert sum(
        test_value
        for test_value, numbers in equations
        if check(test_value, numbers, operators=('+', '*', '||'))
    ) == 145149066755184

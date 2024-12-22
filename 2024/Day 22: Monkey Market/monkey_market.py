"""Day 22: Monkey Market"""


from collections import Counter, deque
from itertools import pairwise, islice


def parse(filename):
    """Parse the input file and return a list of initial secret number
    of each buyer.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return [int(line) for line in f]


def derive(secret):
    """Derive the next secret number from the current secret number."""
    secret = prune(mix(secret * 64, secret))
    secret = prune(mix(secret // 32, secret))
    return prune(mix(secret * 2048, secret))


def mix(value, secret):
    """Mix the value into the secret number."""
    return value ^ secret


def prune(secret):
    """Prune the secret number."""
    return secret % 16777216


def generate(secret):
    """Produces a pseudorandom sequence of secret numbers."""
    yield secret
    while True:
        yield (secret := derive(secret))


def iter_prices(secret):
    """Iterate over the prices."""
    for derived_secret in generate(secret):
        yield derived_secret % 10


def sliding_window(iterable, n):
    """Collect data into overlapping fixed-length chunks or blocks."""
    iterator = iter(iterable)
    window = deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def count(secrets):
    """Count banana for each sequence of four price changes."""
    counter = Counter()
    buyer_prices = [islice(iter_prices(secret), 2000) for secret in secrets]

    for prices in buyer_prices:
        seen = set()
        for (a, b, c, d), (e, f, g, h) in pairwise(sliding_window(prices, 4)):
            seq = e - a, f - b, g - c, h - d
            if seq in seen:
                continue

            seen.add(seq)
            counter[seq] += h

    return counter


def test_example():
    """Test the example."""
    secrets = parse('example1.txt')
    assert sum(
        next(islice(generate(secret), 2000, None))
        for secret in secrets
    ) == 37327623

    secrets = parse('example2.txt')
    counter = count(secrets)
    assert counter.most_common(1) == [((-2, 1, -1, 3), 23)]


def test_puzzle():
    """Test the puzzle."""
    secrets = parse('input.txt')
    assert sum(
        next(islice(generate(secret), 2000, None))
        for secret in secrets
    ) == 20506453102

    counter = count(secrets)
    assert counter.most_common(1) == [((0, 0, -1, 2), 2423)]

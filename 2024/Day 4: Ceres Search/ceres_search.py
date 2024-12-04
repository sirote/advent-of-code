"""Day 4: Ceres Search"""


from contextlib import suppress
from functools import cache


def parse(filename):
    """Parse the word search from a file into a tuple of strings."""
    with open(filename, 'r', encoding='utf-8') as f:
        return tuple(line.strip() for line in f)


def count(word_search, count_fn):
    """Count the number of words in the word search."""
    return sum(
        count_fn(i, j, word_search)
        for i, row in enumerate(word_search)
        for j in range(len(row))
    )


@cache
def to_grid(word_search):
    """Convert the word search into a grid of characters."""
    return tuple(f'{line}.' for line in word_search)


def count_xmas1(i, j, word_search):
    """Count the number of XMAS words at the given position in the word
    search.
    """
    grid = to_grid(word_search)
    word = tuple('XMAS')
    rword = tuple(reversed(word))
    total = 0
    for w in (
        (grid[i][j + k] for k in range(len(word))),
        (grid[i + k][j] for k in range(len(word))),
        (grid[i + k][j + k] for k in range(len(word))),
        (grid[i + k][j - k] for k in range(len(word))),
    ):
        with suppress(IndexError):
            if tuple(w) in (word, rword):
                total += 1

    return total


def count_xmas2(i, j, word_search):
    """Count the number of MAS in the shape of an X at the given
    position in the word search.
    """
    grid = word_search
    out_of_bounds = (
        i < 1
        or j < 1
        or i >= len(grid) - 1
        or j >= len(grid[i]) - 1
    )
    if out_of_bounds:
        return 0

    word = tuple('MAS')
    rword = tuple(reversed(word))
    x = (
        (grid[i - 1][j - 1], grid[i][j], grid[i + 1][j + 1]),
        (grid[i - 1][j + 1], grid[i][j], grid[i + 1][j - 1]),
    )
    if all(w in (word, rword) for w in x):
        return 1
    return 0


def test_example():
    """Test the example."""
    word_search = parse('example.txt')
    assert count(word_search, count_xmas1) == 18
    assert count(word_search, count_xmas2) == 9


def test_puzzle():
    """Test the puzzle."""
    word_search = parse('input.txt')
    assert count(word_search, count_xmas1) == 2297
    assert count(word_search, count_xmas2) == 1745

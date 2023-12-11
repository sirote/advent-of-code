"""Day 11: Cosmic Expansion"""


from itertools import combinations


EMPTY_SPACE = '.'
GALAXY = '#'


def parse(filename):
    """Parse the image data into a grid."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            yield line.strip()


def iter_lengths(universe, expansion_factor=2):
    """Iterate over the lengths between every pair of galaxies."""
    empty_rows, empty_cols = find_empty_spaces(universe)
    for galaxy1, galaxy2 in combinations(iter_galaxies(universe), 2):
        yield (
            length(galaxy1, galaxy2)
            + expanded_length(
                lower=min(galaxy1[0], galaxy2[0]),
                upper=max(galaxy1[0], galaxy2[0]),
                empty_spaces=empty_rows,
                factor=expansion_factor,
            )
            + expanded_length(
                lower=min(galaxy1[1], galaxy2[1]),
                upper=max(galaxy1[1], galaxy2[1]),
                empty_spaces=empty_cols,
                factor=expansion_factor,
            )
        )


def find_empty_spaces(universe):
    """Return row indices and column indices of empty spaces."""
    empty_rows = [
        index
        for index, row in enumerate(universe)
        if all(col == EMPTY_SPACE for col in row)
    ]
    empty_cols = [
        index
        for index, _ in enumerate(universe[0])
        if all(row[index] == EMPTY_SPACE for row in universe)
    ]
    return empty_rows, empty_cols


def iter_galaxies(universe):
    """Iterate over the positions of galaxies."""
    for i, row in enumerate(universe):
        for j, col in enumerate(row):
            if col == GALAXY:
                yield i, j


def length(galaxy1, galaxy2):
    """Return the length of the shortest path between two galaxies."""
    return abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])


def expanded_length(lower, upper, empty_spaces, factor):
    """Return the expanded length of one-dimensional space."""
    return sum(lower < index < upper for index in empty_spaces) * (factor - 1)


def main():
    """Main program."""
    universe = list(parse('input'))
    assert sum(iter_lengths(universe, expansion_factor=2)) == 9623138
    assert sum(iter_lengths(universe, expansion_factor=10**6)) == 726820169514


if __name__ == '__main__':
    main()

"""Day 13: Point of Incidence"""


from itertools import pairwise


def parse(filename):
    """Parse the patterns of ash (.) and rocks (#) into grids."""
    with open(filename, 'r', encoding='utf-8') as file_:
        grid = []
        for line in file_:
            if not line.strip():
                yield grid
                grid = []
            else:
                grid.append(line.strip())

        if grid:
            yield grid


def find_indices(grid, allow_errors=0):
    """Find indices of rows that differ by at most `allow_errors`
    patterns.
    """
    for i, (row1, row2) in enumerate(pairwise(grid)):
        if sum(a != b for a, b in zip(row1, row2)) <= allow_errors:
            yield i


def vertical_reflection(grid, smudges=0):
    """Iterate over indices of first column of vertical reflection
    lines.
    """
    _grid = list(zip(*grid))
    yield from horizontal_reflection(_grid, smudges=smudges)


def horizontal_reflection(grid, smudges=0):
    """Iterate over indices of first row of horizontal reflection
    lines.
    """
    for i in find_indices(grid, allow_errors=smudges):
        _smudges = smudges
        for j, k in zip(range(i + 1, len(grid)), range(i, -1, -1)):
            diff = sum(a != b for a, b in zip(grid[j], grid[k]))
            if diff <= _smudges:
                _smudges -= diff
            else:
                break
        else:
            yield i


def summarize_score(grids, smudges=0):
    """Return the number after summerizing the pattern notes."""
    number = 0
    for grid in grids:
        index = _find_index(vertical_reflection, grid, smudges=smudges)
        if index is not None:
            number += index + 1
            continue

        index = _find_index(horizontal_reflection, grid, smudges=smudges)
        if index is not None:
            number += 100 * (index + 1)

    return number


def _find_index(reflection, grid, smudges=0):
    index = next(reflection(grid), None)
    if smudges:
        index = _find_smudge_index(reflection(grid, smudges=smudges), index)

    return index


def _find_smudge_index(reflections, index):
    for smudge_index in reflections:
        if smudge_index != index:
            index = smudge_index
            break
    else:
        index = None

    return index


def main():
    """Main program."""
    grids = list(parse('input'))
    assert summarize_score(grids) == 29130
    assert summarize_score(grids, smudges=1) == 33438


if __name__ == '__main__':
    main()

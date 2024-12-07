"""Day 6: Guard Gallivant"""


from contextlib import suppress


DIRECTION_MAP = {
    'v': (1, 0),
    '^': (-1, 0),
    '>': (0, 1),
    '<': (0, -1),
}


def parse(filename):
    """Parse the input file and return the guard map and the starting
    position.
    """
    guard_map = []
    start = None
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            guard_map.append(list(line.strip()))
            with suppress(ValueError):
                start = (i, line.index('^'))

    if start is None:
        raise ValueError('No starting position found')

    return guard_map, start


def trace(guard_map, start):
    """Return the positions visited by the guard starting at the given
    position or return None if the guard gets stuck.
    """
    i, j = start
    direction = DIRECTION_MAP[guard_map[i][j]]
    positions = {(start, direction)}

    while True:
        m, n = i + direction[0], j + direction[1]
        if out_of_bounds(guard_map, m, n):
            return positions

        if guard_map[m][n] == '#':
            direction = turn_right(direction)
        else:
            if ((m, n), direction) in positions:
                return None

            positions.add(((m, n), direction))
            i, j = m, n


def out_of_bounds(guard_map, x, y):
    """Return True if the given position is out of bounds."""
    return x < 0 or x >= len(guard_map) or y < 0 or y >= len(guard_map[0])


def turn_right(direction):
    """Return the direction after turning right."""
    return direction[1], -direction[0]


def iter_maps(guard_map, positions):
    """Yield all the maps with the given positions blocked."""
    for x, y in positions:
        temp, guard_map[x][y] = guard_map[x][y], '#'
        yield guard_map
        guard_map[x][y] = temp


def test_example():
    """Test the example."""
    guard_map, start = parse('example.txt')
    positions = {pos for pos, _ in trace(guard_map, start)}
    assert len(positions) == 41
    assert sum(
        trace(m, start) is None
        for m in iter_maps(guard_map, positions - {start})
    ) == 6


def test_puzzle():
    """Test the puzzle."""
    guard_map, start = parse('input.txt')
    positions = {pos for pos, _ in trace(guard_map, start)}
    assert len(positions) == 4967
    assert sum(
        trace(m, start) is None
        for m in iter_maps(guard_map, positions - {start})
    ) == 1789

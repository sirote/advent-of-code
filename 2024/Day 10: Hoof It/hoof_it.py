"""Day 10: Hoof It"""


from itertools import product


def parse(filename):
    """Parse the input file and return the topo map, start and end
    points.
    """
    topo_map = []
    starts = []
    ends = []
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            topo_map.append([int(h) for h in line.strip()])
            for j, h in enumerate(line):
                if h == '0':
                    starts.append((i, j))
                elif h == '9':
                    ends.append((i, j))

    return topo_map, starts, ends


def score(topo_map, start, end, distinct=False):
    """Return the score of a trailhead."""
    count = 0
    queue = [start]
    while queue:
        x, y = queue.pop()
        for m, n in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
            if (
                m < 0
                or n < 0
                or m >= len(topo_map)
                or n >= len(topo_map[0])
            ):
                continue

            if topo_map[m][n] - topo_map[x][y] != 1:
                continue

            if (m, n) == end:
                count += 1
                if distinct:
                    continue
                return count

            queue.append((m, n))

    return count


def test_example():
    """Test the example."""
    topo_map, starts, ends = parse('example.txt')
    assert sum(
        score(topo_map, start, end)
        for start, end in product(starts, ends)
    ) == 36
    assert sum(
        score(topo_map, start, end, distinct=True)
        for start, end in product(starts, ends)
    ) == 81


def test_puzzle():
    """Test the puzzle."""
    topo_map, starts, ends = parse('input.txt')
    assert sum(
        score(topo_map, start, end)
        for start, end in product(starts, ends)
    ) == 517
    assert sum(
        score(topo_map, start, end, distinct=True)
        for start, end in product(starts, ends)
    ) == 1116

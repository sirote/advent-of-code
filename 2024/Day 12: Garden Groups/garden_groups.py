"""Day 12: Garden Groups"""


from collections import defaultdict


def parse(filename):
    """Parse the garden map from a file."""
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()


def iter_regions(garden_map):
    """Iterate over all regions in the garden map."""
    visited = set()

    for i in range(len(garden_map)):
        for j in range(len(garden_map[0])):
            if (i, j) in visited:
                continue

            yield (region := _get_region(garden_map, (i, j)))
            visited.update(region)


def neighbors(x, y):
    """Iterate over the neighbors of a garden plot."""
    for m, n in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
        yield m, n


def _get_region(garden_map, pos):
    region = {pos}
    queue = [pos]
    while queue:
        x, y = queue.pop()
        for m, n in _neighbor_plots(garden_map, x, y):
            if (m, n) in region:
                continue

            region.add((m, n))
            queue.append((m, n))

    return region


def _neighbor_plots(garden_map, x, y):
    for m, n in neighbors(x, y):
        if m < 0 or m >= len(garden_map) or n < 0 or n >= len(garden_map[0]):
            continue

        if garden_map[m][n] != garden_map[x][y]:
            continue

        yield m, n


def area(region):
    """Return the area of a region."""
    return len(region)


def perimeter1(region):
    """Return the perimeter of a region.

    The perimeter of a region is the number of sides of garden plots in
    the region that do not touch another garden plot in the same region.
    """
    return sum(
        plot not in region
        for x, y in region
        for plot in neighbors(x, y)
    )


def perimeter2(region):
    """Return the perimeter of a region.

    The perimeter of a region is the number of sides each region has.
    """
    perimeter = 0
    direction_map = defaultdict(set)

    for x, y in sorted(region):
        for d, (m, n) in enumerate(sorted(neighbors(x, y))):
            if (m, n) in region:
                continue

            directions = direction_map[d]
            directions.add((m, n))

            match d:
                case 0 | 3 if (m, n - 1) not in directions:
                    perimeter += 1
                case 1 | 2 if (m - 1, n) not in directions:
                    perimeter += 1

    return perimeter


def cost(garden_map, perimeter):
    """Return the cost of fence required to enclose all regions."""
    return sum(
        area(region) * perimeter(region)
        for region in iter_regions(garden_map)
    )


def test_example():
    """Test the example."""
    test_inputs = (
        ('example1.txt', 140),
        ('example2.txt', 772),
        ('example5.txt', 1930),
    )
    for example, expected in test_inputs:
        garden_map = list(parse(example))
        assert cost(garden_map, perimeter1) == expected

    test_inputs = (
        ('example1.txt', 80),
        ('example2.txt', 436),
        ('example3.txt', 236),
        ('example4.txt', 368),
        ('example5.txt', 1206),
    )
    for example, expected in test_inputs:
        garden_map = list(parse(example))
        assert cost(garden_map, perimeter2) == expected


def test_puzzle():
    """Test the puzzle."""
    garden_map = list(parse('input.txt'))
    assert cost(garden_map, perimeter1) == 1449902
    assert cost(garden_map, perimeter2) == 908042

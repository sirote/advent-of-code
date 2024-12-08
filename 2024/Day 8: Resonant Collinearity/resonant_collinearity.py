"""Day 8: Resonant Collinearity"""


from collections import defaultdict
from itertools import chain, combinations, count


def parse(filename):
    """Parse the input file and return the antenna map and locations."""
    antenna_map = []
    antenna_to_locations = defaultdict(list)

    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.strip()
            antenna_map.append(line)
            for j, x in enumerate(line):
                if x == '.':
                    continue
                antenna_to_locations[x].append((i, j))

    return antenna_map, antenna_to_locations


def find_antinodes(antenna_map, antenna_to_locations,
                   resonant_harmonics=False):
    """Return the set of antinodes that is perfectly in line with two
    antennas of the same frequency - but only when one of the antennas
    is twice as far away as the other when resonant_harmonics is False.
    """
    return {
        antinode
        for locations in antenna_to_locations.values()
        for loc1, loc2 in combinations(locations, 2)
        for antinode in chain.from_iterable(
            antinode_iterators(
                loc1,
                loc2,
                antenna_map,
                resonant_harmonics=resonant_harmonics,
            )
        )
    }


def antinode_iterators(loc1, loc2, antenna_map, resonant_harmonics=False):
    """Return two iterators that yield antinodes in opposite
    directions.
    """
    dx = loc2[0] - loc1[0]
    dy = loc2[1] - loc1[1]
    loop = count if resonant_harmonics else range

    def iterator1(loc):
        for _ in loop(1):
            loc = (loc[0] - dx, loc[1] - dy)
            if out_of_bounds(loc, antenna_map):
                break
            yield loc

    def iterator2(loc):
        for _ in loop(1):
            loc = (loc[0] + dx, loc[1] + dy)
            if out_of_bounds(loc, antenna_map):
                break
            yield loc

    return iterator1(loc1), iterator2(loc2)


def out_of_bounds(loc, antenna_map):
    """Return True if the location is out of bounds."""
    return (
        loc[0] < 0
        or loc[0] >= len(antenna_map)
        or loc[1] < 0
        or loc[1] >= len(antenna_map[0])
    )


def test_example():
    """Test the example."""
    antenna_map, antenna_to_locations = parse('example.txt')
    assert len(find_antinodes(antenna_map, antenna_to_locations)) == 14

    antennas = set(chain.from_iterable(antenna_to_locations.values()))
    assert len(
        antennas | find_antinodes(
            antenna_map,
            antenna_to_locations,
            resonant_harmonics=True,
        )
    ) == 34


def test_puzzle():
    """Test the puzzle."""
    antenna_map, antenna_to_locations = parse('input.txt')
    assert len(find_antinodes(antenna_map, antenna_to_locations)) == 285

    antennas = set(chain.from_iterable(antenna_to_locations.values()))
    assert len(
        antennas | find_antinodes(
            antenna_map,
            antenna_to_locations,
            resonant_harmonics=True,
        )
    ) == 944

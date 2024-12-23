"""Day 20: Race Condition"""


import math
from collections import Counter, deque
from typing import NamedTuple


class RaceTrack(NamedTuple):
    """A racetrack with start and end positions."""

    map: list
    start: tuple
    end: tuple

    @property
    def width(self):
        """Return the width of the racetrack."""
        return len(self.map[0])

    @property
    def height(self):
        """Return the height of the racetrack."""
        return len(self.map)


def parse(filename):
    """Parse the racetrack from a file."""
    map_ = []
    start = end = None

    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.strip()
            map_.append(line)
            for j, cell in enumerate(line):
                if cell == 'S':
                    start = (i, j)
                elif cell == 'E':
                    end = (i, j)

    if start is None or end is None:
        raise ValueError("Start or end not found in the racetrack")

    return RaceTrack(tuple(map_), start, end)


def distances(racetrack, start=None, wall=True, max_dist=math.inf):
    """Yield all positions and their distances from the start."""
    queue = deque([(start or racetrack.start, 0)])
    visited = set()

    while queue:
        pos, dist = queue.popleft()
        if dist > max_dist:
            continue

        if pos in visited:
            continue

        visited.add(pos)
        yield pos, dist

        x, y = pos
        for m, n in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
            if (
                m < 0
                or n < 0
                or m >= racetrack.height
                or n >= racetrack.width
            ):
                continue

            if wall and racetrack.map[m][n] == '#':
                continue

            queue.append(((m, n), dist + 1))


def cheat_tracks(racetrack, max_dist):
    """Yield all possible cheat tracks."""
    for start, _ in distances(racetrack):
        for end, dist in distances(
                racetrack, start, wall=False, max_dist=max_dist):
            if end == start:
                continue

            if racetrack.map[end[0]][end[1]] == '#':
                continue

            yield (start, end), dist


def count_cheats(racetrack, max_dist, save=0):
    """Count the number of possible cheats."""
    dists = dict(distances(racetrack))
    normal_dist = dists[racetrack.end]
    cheats = {}

    for cheat, cheat_dist in cheat_tracks(racetrack, max_dist):
        dist = (
            dists[cheat[0]]
            + cheat_dist
            + normal_dist
            - dists[cheat[1]]
        )
        if dist + save > normal_dist:
            continue

        cheats[cheat] = min(cheats.get(cheat, math.inf), dist)

    return Counter(cheats.values())


def test_example():
    """Test the example."""
    racetrack = parse('example.txt')
    counter = count_cheats(racetrack, 2, save=1)
    assert counter.total() == 44

    counter = count_cheats(racetrack, 20, save=50)
    assert counter.total() == 285


def test_puzzle():
    """Test the puzzle."""
    racetrack = parse('input.txt')
    counter = count_cheats(racetrack, 2, save=100)
    assert counter.total() == 1448

    counter = count_cheats(racetrack, 20, save=100)
    assert counter.total() == 1017615
